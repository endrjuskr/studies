
/* 01 */        #define N	3                           /* liczba procesow */
/* 02 */        bool chce[N], we[N], wy[N], visited_waiting_room[N], started_prolog[N], reseted[N];
                byte counter_critical_section = 0;                           /* licznik procesow w sekcji krytycznej */
                int counter_critical_section_for_process[N];                      /* licznik procesow ktore weszly do sekcji krytycznej po rozpoczeciu prologu przez proces */
/* 03 */        #define i _pid
                #define restart if :: true -> true; :: true -> goto reset_process fi;

/* 04 */        active [N] proctype P()
/* 05 */        {
                    int k = 0;
/* 06 */        start:

                    if
                        :: true -> true
                        :: true -> false
                    fi;
  
                prolog:
                    //reseted[i] = false;
                
                    atomic {
/* 07 */            chce[i] = true;
                    //visited_waiting_room[i] = false;
                    started_prolog[i] = true;
                    }
                
                    restart
                before_waiting_room: 
                    k = 0;
                    do
	                    :: k == N -> break
                        :: k < N && !(chce[k] && we[k]) -> k++;
                        :: else -> goto before_waiting_room;
                    od; 
		  
                    restart
/* 08 */            we[i] = true;
                    restart

                try_to_ommit_waiting_room:
                    k = 0;
                    do
                        :: k == N -> goto after_waiting_room;
                        :: k < N && chce[k] && !we[k] -> goto waiting_room;
                        :: else -> k++;
                    od;                  
                waiting_room:
/* 09 */            {    
                        restart
                        //visited_waiting_room[i] = true;
/* 10 */                chce[i] = false;
                        restart
                inside_waiting_room:
                        k = 0;
		                do
                            :: ( k < N && !wy[k] && chce[k] && !we[k]) -> k++;
                            :: else -> goto leaving_waiting_room
		                od;
                leaving_waiting_room:
                        restart
/* 11 */                chce[i] = true;
                        if
                                :: (!wy[k]) -> goto try_to_ommit_waiting_room;
                                :: else -> skip; 
                        fi;
                        restart
/* 12 */            }
                after_waiting_room: 
                    restart
/* 13 */            wy[i] = true;
                    restart
                wait_for_leaving_waiting_room:
	                k = i + 1;
                    do
              		 	:: k == N -> break;
                        :: k < N && !(!we[k] || wy[k]) -> goto wait_for_leaving_waiting_room;
                        :: else -> k++;
	                od;

                    restart

	            wait_for_critical_section:
                    k = 0;
	                do
          		    	:: k == i -> break;
                        :: k < i && we[k] -> goto wait_for_critical_section;
                        :: else -> k++;
                    od;

                    restart
                sk:
                    counter_critical_section++;
                        
                    k = 0;
                    do
                        :: k < N && started_prolog[k] -> { counter_critical_section_for_process[k]++; k++; }
                        :: k == N -> break;
                        :: else -> k++;
                    od; 

                    counter_critical_section_for_process[i] = 0;
                    started_prolog[i] = false;
                    /* SEKCJA KRYTYCZNA */
                    counter_critical_section--;

                    atomic {                    
/* 14 */            wy[i] = false; 
                          
/* 15 */            we[i] = false;
/* 16 */            chce[i] = false;
                    }

/* 17 */            goto start;
                reset_process:
                    atomic
                    {
                        reseted[i] = true;
                        we[i] = false; 
                        wy[i] = false; 
                        chce[i] = false; 
                        visited_waiting_room[i] = false; 
                        started_prolog[i] = false; 
                        counter_critical_section_for_process[i] = 0;
                    }

                wait_before_start:
                    k = 0;
                    do
                        :: k == N -> break;
                        :: else
                            if 
                                :: !we[k] || wy[k] -> k++;
                            fi;
                    od; 

                    goto start;
/* 18 */        }



/* ltl wzajemne_wykluczanie { [] ( counter_critical_section < 2 ) } */
/* ltl nieunikniona_poczekalnia { [] ( P[0]@sk -> visited_waiting_room[0] ) } */
/* ltl wyjscie_z_poczekalni { [] ( ( we[0] && !chce[0] ) -> <> ( wy[1] || wy[2] || wy[3] ) ) } */
/* ltl brak_zaglodzenia { []( P[0]@prolog -> <> P[0]@sk ) } */
ltl liniowosc { [] ( counter_critical_section_for_process[0] <= 2*N ) }