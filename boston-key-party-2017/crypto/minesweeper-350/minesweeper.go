package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"io/ioutil"
	"math"
	"math/cmplx"
	"math/rand"
	"net"
)

type UserError struct {
	msg string // description of error
}

func (e *UserError) Error() string { return e.msg }

const (
	G_I = 0 // Identity
	G_X = 1 // Pauli X-gate
	G_Y = 2 // Pauli Y-gate
	G_Z = 3 // Pauli Z-gate
	G_H = 4 // Hadamard gate
	G_R = 5 // R2 gate: rotate phase by 90 degrees
	G_P = 6 // Rotate phase by an angle specified in radians
	G_M = 7 // Measure in standard (Z) basis, and if 1, self-destruct
)

var S float64 = math.Sqrt(0.5)

var flag []byte

var MATRICES = [6][2][2]complex128{
	{{complex(1, 0), complex(0, 0)}, {complex(0, 0), complex(1, 0)}},
	{{complex(0, 0), complex(1, 0)}, {complex(1, 0), complex(0, 0)}},
	{{complex(0, 0), complex(0, -1)}, {complex(0, 1), complex(0, 0)}},
	{{complex(1, 0), complex(0, 0)}, {complex(0, 0), complex(-1, 0)}},
	{{complex(S, 0), complex(S, 0)}, {complex(S, 0), complex(-S, 0)}},
	{{complex(1, 0), complex(0, 0)}, {complex(0, 0), complex(0, 1)}},
}

func apply_gate(state [4]complex128, matrix [2][2]complex128, wire bool, controlled bool) [4]complex128 {
	var result [4]complex128
	// I could carefully parameterize this.  Or I could be a lazy bum!
	if wire && controlled {
		result[0] = state[0]
		result[2] = state[2]
		result[1] = matrix[0][0]*state[1] + matrix[1][0]*state[3]
		result[3] = matrix[0][1]*state[1] + matrix[1][1]*state[3]
	} else if wire {
		result[0] = matrix[0][0]*state[0] + matrix[1][0]*state[2]
		result[2] = matrix[0][1]*state[0] + matrix[1][1]*state[2]
		result[1] = matrix[0][0]*state[1] + matrix[1][0]*state[3]
		result[3] = matrix[0][1]*state[1] + matrix[1][1]*state[3]
	} else if controlled {
		result[0] = state[0]
		result[1] = state[1]
		result[2] = matrix[0][0]*state[2] + matrix[1][0]*state[3]
		result[3] = matrix[0][1]*state[2] + matrix[1][1]*state[3]
	} else {
		result[0] = matrix[0][0]*state[0] + matrix[1][0]*state[1]
		result[1] = matrix[0][1]*state[0] + matrix[1][1]*state[1]
		result[2] = matrix[0][0]*state[2] + matrix[1][0]*state[3]
		result[3] = matrix[0][1]*state[2] + matrix[1][1]*state[3]
	}
	return result
}

func measure_wire(state [4]complex128, wire bool) [4]complex128 {
	prob_zero := cmplx.Abs(state[0]) * cmplx.Abs(state[0])
	if wire {
		prob_zero += cmplx.Abs(state[1]) * cmplx.Abs(state[1])
	} else {
		prob_zero += cmplx.Abs(state[2]) * cmplx.Abs(state[2])
	}
	if rand.Float64() < prob_zero {
		var result [4]complex128
		result[0] = state[0] / complex(math.Sqrt(prob_zero), 0)
		result[3] = complex(0, 0)
		if wire {
			result[1] = state[1] / complex(math.Sqrt(prob_zero), 0)
			result[2] = complex(0, 0)
		} else {
			result[1] = complex(0, 0)
			result[2] = state[2] / complex(math.Sqrt(prob_zero), 0)
		}
		return result
	} else {
		panic(UserError{"BOOM!"})
	}
}

func measure_final(state [4]complex128) int {
	var so_far float64 = 0
	actual := rand.Float64()
	for i := 0; i < 4; i++ {
		so_far += cmplx.Abs(state[i]) * cmplx.Abs(state[i])
		if so_far >= actual {
			return i
		}
	}
	panic(UserError{"Bad probability?"})
}

func handle_connection(conn net.Conn) {
	defer func() {
		e := recover()
		if e != nil {
			if uerr, ok := e.(UserError); ok {
				fmt.Println(uerr.Error())
				conn.Write([]byte(uerr.Error()))
			}
		}
		conn.Close()
	}()

	bombs := make([]bool, 14*8)
	for ix := range bombs {
		bombs[ix] = (rand.Intn(2) == 1)
	}
	for {
		command := make([]byte, 2)
		io.ReadFull(conn, command)
		num_gates := uint16(command[1]) + 256*uint16(command[0])
		if num_gates == 0 {
			break
		}
		state := [4]complex128{complex(1, 0), complex(0, 0), complex(0, 0), complex(0, 0)}
		for i := uint16(0); i < num_gates; i++ {
			gates := make([]byte, 1)
			io.ReadFull(conn, gates)
			gate := gates[0]
			primary_wire := (gate & 0x80) != 0
			var gate_id byte
			var controlled bool
			if (gate & 0x7F) < 0x70 {
				controlled = false
				if bombs[gate&0x7F] {
					gate_id = G_M
				} else {
					gate_id = G_I
				}
			} else {
				controlled = (gate & 0x08) != 0
				gate_id = (gate & 0x07)
			}

			if gate_id == G_M {
				// Can't control a measurement!  Ignore 'controlled' flag
				state = measure_wire(state, primary_wire)
			} else {
				var matrix [2][2]complex128
				if gate_id == G_P {
					// Phase gate in radians
					bytes := make([]byte, 8)
					io.ReadFull(conn, bytes)
					bits := binary.LittleEndian.Uint64(bytes)
					imag_part := math.Float64frombits(bits)
					factor := cmplx.Exp(complex(0, imag_part))
					matrix = [2][2]complex128{{complex(1, 0), complex(0, 0)}, {complex(0, 0), factor}}
				} else {
					matrix = MATRICES[gate_id]
				}
				state = apply_gate(state, matrix, primary_wire, controlled)
			}
		}
		res := byte(measure_final(state))
		conn.Write([]byte{res})
	}
	guess := make([]byte, 14)
	io.ReadFull(conn, guess)
	for ix, g := range guess {
		for i := 0; i < 8; i++ {
			var theirs bool = (g & (0x01 << uint16(7-i))) != 0
			var ours bool = bombs[ix*8+i]
			if theirs != ours {
				panic(UserError{"WRONG"})
			}
		}
	}
	conn.Write(flag)
	conn.Close()
}

func main() {
	key, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(string(key))
	flag = key
	if len(flag) > 50 {
		panic(UserError{"this doesn't happen"})
	}
	listener, err := net.Listen("tcp", "0.0.0.0:8001")
	if err != nil {
		panic(err)
	}
	defer listener.Close()
	fmt.Println("Ready to rumble.")
	for {
		conn, err := listener.Accept()
		if err != nil {
			panic(err)
		}
		go handle_connection(conn)
	}
}
