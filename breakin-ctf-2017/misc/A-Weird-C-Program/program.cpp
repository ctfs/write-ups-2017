#include     			 	  <stdio.h>
#include	<string.h>
#include     		 	   <bits/stdc++.h>
#include	<codeme.h>
/*int     main(		int argc, char	**argv 	)
{*/	
#define     	EEr_Rs 					0x4b
#include	<stdlib.h>
#include     		  		 <sys/socket.h>
#include	<netinet/in.h>
#define     	LINE_new	 		  '\n'
#include	<assert.h>
#include     		    	<time.h>
#include	<sys/types.h>
#include     		  			<arpa/inet.h>
#include	<netdb.h>
#include     	 					<unistd.h>
	
int main(){ int run;  		 	  	
	run>>=5;run=0;
    run&=01; 		int	FELICITY[10000];  		
	run>>=5;
     using	namespace std;					
	
     	 	 			
	
char *res[6] = {"Nothing_"  			    ,
	
" and _no _one _is _perfect.	 	 	 	",
	
     "It_	just _takes_    a_good	_eye_",
	
     	  	  "to_find_"	,
	
     		"those_	hidden_" 	  ,
	
     			"imperfections. :)" 		};
	
     		int i = 0,j=0; 	
	
     		for( i=0;i <	6 ; i++)for(j=0;j<strlen(res[i]);j++)
	
     		{int t=(int)res[i][j];if(t	==	'_' )FELICITY[run++]=32;else	if((t==32||t==9)&&(j!=27))FELICITY[run++]=-1;
	
     		else FELICITY[run++]=	t   ;}
	
     		for( i=0; i< run ;i++	)
	
     		 	if(FELICITY[i]+1)printf("%c",(char)FELICITY[i]); i-=1		;
	
     	 printf("\n")	 ;
	
return  0;
 } 



/*END*/

