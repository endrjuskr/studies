
/* 01 */        #define N	4                           /* liczba procesow */
/* 02 */        bool chce[N], we[N], wy[N], visited_waiting_room[N], started_prolog[N];
                byte counter_critical_section = 0;                           /* licznik procesow w sekcji krytycznej */
                int counter_critical_section_for_process[N];                      /* licznik procesow ktore weszly do sekcji krytycznej po rozpoczeciu prologu przez proces */
/* 03 */        #define i _pid

/* 04 */        active [N] proctype P()
/* 05 */        {
                    int k = 0;
/* 06 */        start:

                    if
                        :: true -> true
                        :: true -> false
                    fi;
  
                prolog:
/* 07 */            chce[i] = true;
                    visited_waiting_room[i] = false;
                    started_prolog[i] = true;
                before_waiting_room: 
                    k = 0;
                    do
	                    :: k >= N -> break
                        :: k < N && !(chce[k] && we[k]) -> k++;
                        :: else -> goto before_waiting_room;
                    od; 
		

/* 08 */            we[i] = true;
                    k = 0;

                    do
                        :: k >= N -> goto after_waiting_room;
                        :: k < N && chce[k] && !we[k] -> goto waiting_room;
                        :: else -> k++;
                    od;                  
                waiting_room:
/* 09 */            {    
                        visited_waiting_room[i] = true;
/* 10 */                chce[i] = false;
                inside_waiting_room:
		                k = 0;
		                do
                            :: k == N -> goto inside_waiting_room;
                            :: k < N && wy[k] -> goto leaving_waiting_room;
		                    :: else -> k++;
		                od;
                leaving_waiting_room:
                      
/* 11 */                chce[i] = true;
/* 12 */            }
                after_waiting_room: 
/* 13 */                wy[i] = true;

                wait_for_leaving_waiting_room:
		                k = i + 1;
                    do
              		 	:: k == N -> break;
                        :: k < N && !(!we[k] || wy[k]) -> goto wait_for_leaving_waiting_room;
                        :: else -> k++;
	                od;

	            wait_for_critical_section:
                    k = 0;
	                do
          		    	:: k == i -> break;
                        :: k < i && we[k] -> goto wait_for_critical_section;
                        :: else -> k++;
                    od;
                sk:
                    counter_critical_section++;
                    atomic {    
                    k = 0;
                    do
                        :: k < N && started_prolog[k] -> { counter_critical_section_for_process[k]++; k++; }
                        :: k == N -> break;
                        :: else -> k++;
                    od; 

                    counter_critical_section_for_process[i] = 0;
                    }
                    started_prolog[i] = false;
                    /* SEKCJA KRYTYCZNA */
                    counter_critical_section--;

/* 15 */            we[i] = false;
/* 14 */            wy[i] = false; 
/* 16 */            chce[i] = false;

/* 17 */            goto start;
/* 18 */        }



/* ltl wzajemne_wykluczanie { [] ( counter_critical_section < 2 ) } */
/* ltl nieunikniona_poczekalnia { [] ( P[0]@sk -> visited_waiting_room[0] ) } */
/* ltl wyjscie_z_poczekalni { [] ( ( we[0] && !chce[0] ) -> <> ( wy[1] || wy[2] || wy[3] ) ) } */
/* ltl brak_zaglodzenia { []( P[0]@prolog -> <> P[0]@sk ) } */
ltl liniowosc { [] ( counter_critical_section_for_process[0] <= N ) }