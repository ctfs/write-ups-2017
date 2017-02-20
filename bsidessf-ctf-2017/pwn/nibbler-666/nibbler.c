#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>

#define disable_buffering(_fd) setvbuf(_fd, NULL, _IONBF, 0)

/* Note: It's important that these are prime numbers, otherwise it might be
 * impossible to build shellcode. */
#define BOARD_WIDTH 23
#define BOARD_HEIGHT 19

#define STARTING_MAX_LENGTH 16
#define CODE_LENGTH 1024

static int delay = 500000;

typedef struct {
  ssize_t row;
  ssize_t col;
  char direction;
} coords_t;

typedef enum {
  SCORE_STATE_LEFT,
  SCORE_STATE_RIGHT
} score_state_t;

/* The global state. */
typedef struct {
  coords_t prize;
  uint8_t prize_value;

  /* This will be an array that's expanded as time goes on. */
  coords_t *snake;
  ssize_t snake_length;
  ssize_t snake_max_length;
  char snake_direction;
  int is_growing;

  /* A random obstacle, to make things a little trickier. */
  coords_t obstacle;

  /* The score array. */
  uint8_t *scores;
  ssize_t score_num;
  score_state_t score_state;

  /* The UI thread. */
  pthread_t ui_thread;
} state_t;
static state_t state;

static void print_times(char c, ssize_t times)
{
  ssize_t i;

  for(i = 0; i < times; i++)
    printf("%c", c);
}

static void print_character_at(ssize_t row, ssize_t col)
{
  ssize_t i;

  /* Check if we're printing the prize. */
  if(row == state.prize.row && col == state.prize.col) {
    if(state.score_state == SCORE_STATE_LEFT)
      printf("%x0", state.prize_value);
    else
      printf("0%x", state.prize_value);

    return;
  }

  /* Check if we're printing the snake's head. */
  if(row == state.snake[0].row && col == state.snake[0].col) {
    printf("@@");
    return;
  }

  if(row == state.obstacle.row && col == state.obstacle.col) {
    printf("**");
    return;
  }

  /* Check if we're printing the snake's body. */
  for(i = 1; i < state.snake_length; i++) {
    if(row == state.snake[i].row && col == state.snake[i].col) {
      printf("oo");
      return;
    }
  }

  /* Print an empty space. */
  printf("  ");
}

static void draw_board()
{
  ssize_t row, col;
  int i;

  /* Print the score. */
  printf("Score: ");
  for(i = 0; i < state.score_num; i++) {
    printf("%02x ", state.scores[i]);
  }
  if(state.score_state == SCORE_STATE_RIGHT)
    printf("%x?", state.scores[state.score_num] >> 4);
  printf("\n\n");

  /* Top. */
  printf("+");
  print_times('^', BOARD_WIDTH * 2);
  printf("+");
  printf("\n");

  /* Rows. */
  for(row = 0; row < BOARD_HEIGHT; row++) {
    printf("<");
    for(col = 0; col < BOARD_WIDTH; col++) {
      print_character_at(row, col);
    }
    printf(">");
    printf("\n");
  }

  /* Bottom. */
  printf("+");
  print_times('v', BOARD_WIDTH * 2);
  printf("+");
  printf("\n");
  printf("Directions: (gotta press <enter> after)\n");
  printf("w = up\n");
  printf("a = left\n");
  printf("s = down\n");
  printf("d = right\n");
  printf("\n");
}

static coords_t dir_to_move(char dir) {
  coords_t result;
  result.row = 0;
  result.col = 0;

  switch(dir) {
    case 'w':
      result.row = -1;
      break;

    case 'a':
      result.col = -1;
      break;

    case 's':
      result.row = 1;
      break;

    case 'd':
      result.col = 1;
      break;
  }

  return result;
}

static ssize_t increment(ssize_t value, ssize_t direction, ssize_t max)
{
  value += direction;

  if(value >= max)
    value = 0;
  else if(value < 0)
    value = max - 1;

  return value;
}

static void move_snake() {
  int i;
  coords_t segment_move;

  /* Move the body. */
  if(state.is_growing) {
    /* Shift everything back by 1, except for the head. */
    for(i = state.snake_length - 1; i > 0; i--) {
      state.snake[i].row = state.snake[i-1].row;
      state.snake[i].col = state.snake[i-1].col;
      state.snake[i].direction = state.snake[i-1].direction;
    }

    /* Move the head. */
    segment_move = dir_to_move(state.snake_direction);
    state.snake[0].row = increment(state.snake[0].row, segment_move.row, BOARD_HEIGHT);
    state.snake[0].col = increment(state.snake[0].col, segment_move.col, BOARD_WIDTH);
    state.snake[0].direction = state.snake_direction; /* TODO: I don't think this line matters. */
    state.is_growing = 0;
  } else {
    for(i = state.snake_length - 1; i > 0; i--) {
      segment_move = dir_to_move(state.snake[i-1].direction);
      state.snake[i].row = increment(state.snake[i].row, segment_move.row, BOARD_HEIGHT);
      state.snake[i].col = increment(state.snake[i].col, segment_move.col, BOARD_WIDTH);
      state.snake[i].direction = state.snake[i-1].direction;
    }

    /* Move the head. */
    segment_move = dir_to_move(state.snake_direction);
    state.snake[0].row = increment(state.snake[0].row, segment_move.row, BOARD_HEIGHT);
    state.snake[0].col = increment(state.snake[0].col, segment_move.col, BOARD_WIDTH);
    state.snake[0].direction = state.snake_direction;
  }
}

static void place_prize()
{
  state.prize.row = rand() % BOARD_HEIGHT;
  state.prize.col = rand() % BOARD_WIDTH;
  state.prize_value = rand() & 0x0F;

  do {
    state.obstacle.row = rand() % BOARD_HEIGHT;
    state.obstacle.col = rand() % BOARD_WIDTH;
  } while(state.obstacle.row == state.prize.row && state.obstacle.col == state.prize.col);
}

static int check_collision()
{
  ssize_t i;

  /* Check if they're on top of a number. */
  if(state.snake[0].row == state.prize.row && state.snake[0].col == state.prize.col) {
    /* Grow the snake. */
    state.snake_length += 1;
    state.is_growing = 1;

    /* Allocate more room for the body if needed. */
    if(state.snake_length >= state.snake_max_length) {
      state.snake_max_length = state.snake_max_length * 2;
      state.snake = realloc(state.snake, sizeof(coords_t) * state.snake_max_length);
    }

    /* Start the last segment start to a bad value - it'll be updated as soon
       as it moves, we just don't want it to be drawn yet. */
    state.snake[state.snake_length - 1].row = -1;
    state.snake[state.snake_length - 1].col = -1;

    if(state.score_state == SCORE_STATE_LEFT)
    {
      state.score_state = SCORE_STATE_RIGHT;
      state.scores[state.score_num] = state.prize_value << 4;
    }
    else
    {
      state.score_state = SCORE_STATE_LEFT;
      state.scores[state.score_num] |= state.prize_value;
      state.score_num++;
    }

    place_prize();

    return 0;
  }

  /* Check if they're out of bounds. */
#if 0
  if(state.snake[0].row < 0 || state.snake[0].col < 0 || state.snake[0].row >= BOARD_HEIGHT || state.snake[0].col >= BOARD_WIDTH) {
    printf("Ouch! You hit a wall!\n");
    return 1;
  }
#endif

  /* Check if they hit themselves. */
  for(i = 1; i < state.snake_length; i++) {
    if(state.snake[0].row == state.snake[i].row && state.snake[0].col == state.snake[i].col) {
      printf("Ouch! You hit yourself!\n");
      return 1;
    }
  }

  /* Check if the hit the obstacle. */
  if(state.snake[0].row == state.obstacle.row && state.snake[0].col == state.obstacle.col) {
    return 1;
  }

  return 0;
}

static void *ui_thread(void *direction_ptr) {
  for(;;) {
    char move = getchar();

    if(move == 'w' || move == 'a' || move == 's' || move == 'd') {
      *((char*)direction_ptr) = move;
    }
  }
  return NULL;
}

void init()
{
  char str_delay[16];

  printf("How many microseconds of delay would you like, per tick? [500000]\n");
  printf("> ");
  fflush(stdout);
  read(fileno(stdin), str_delay, 16);
  str_delay[15] = '\0';
  delay = atoi(str_delay);
  if(delay <= 0)
    delay = 500000;

  srand(time(NULL));

  place_prize(&state);
  state.snake_max_length = STARTING_MAX_LENGTH;
  state.snake = (coords_t*) malloc(sizeof(coords_t) * STARTING_MAX_LENGTH);

  state.snake_length = 1;
  state.snake[0].row = rand() % BOARD_HEIGHT;
  state.snake[0].col = rand() % BOARD_WIDTH;
  state.snake_direction = 's';
  state.score_num = 0;
}

int main(int argc, char *argv[])
{
  disable_buffering(stdout);
  disable_buffering(stderr);

  init();
  state.scores = mmap(NULL, CODE_LENGTH, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
  state.score_state = SCORE_STATE_LEFT;

  /* Create a UI thread. */
  if(pthread_create(&state.ui_thread, NULL, ui_thread, &state.snake_direction)) {
    printf("Error creating thread\n");
    return 1;
  }

  for(;;) {
    draw_board(&state);

    state.prize_value = (state.prize_value + 1) & 0x0F;

    /* The delay. which has to come after drawing the board but before moving
     * the snake. */
    usleep(delay);

    move_snake(&state);

    if(check_collision(&state))
      break;

  }

  alarm(10);

  printf("Thanks for playing!\n");
  asm("call *%0\n" : :"r"(state.scores));

  return 0;
}
