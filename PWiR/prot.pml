
/* 01 */        #define N	4                           /* liczba procesow */
/* 02 */        bool chce[N], we[N], wy[N], was_pocz[N], prolog[N];
                byte csk = 0;
                int sk_counter[N];
/* 03 */        #define i _pid

/* 04 */        active [N] proctype P()
/* 05 */        {
                    int counter = 0;
/* 06 */        start:

                    /*if
                        :: true -> true
                        :: true -> false
                    fi; */
  
                prot:
/* 07 */            chce[i] = true;
                    was_pocz[i] = false;
                    prolog[i] = true;
                L1: 
                    counter = 0;
                    do
		                    :: counter >= N -> break
                        :: else -> 
                        if
                            :: !(chce[counter] && we[counter]) -> counter++;
                            :: else -> goto L1;
                        fi;
                    od; 
		

/* 08 */            we[i] = true;
                    counter = 0;

                    /* TODO: jesli dla pewnego k z [0..N-1] zachodzi chce[k] && !we[k], to wykonaj 09..12, wpp. idź do 13 */
                    do
                        :: counter >= N -> goto L4
                        :: else -> 
                            if 
                                :: (chce[counter] && !we[counter]) -> goto L3
                                :: else -> counter++;
                            fi;
                    od;                  
                L3:
/* 09 */            {    
                        was_pocz[i] = true;
/* 10 */                chce[i] = false;
                L5:
				                counter = 0;
				                do
				                    :: counter >= N -> goto L5
                            :: else ->
                                if
    					                     :: wy[counter] -> goto L10;
					                         :: else -> counter++;
                                fi;
				                od;
                        goto L5;
                L10:            /* TODO: czekaj, az dla pewnego k z [0..N-1] zachodzi wy[k] */
                      
/* 11 */                chce[i] = true;
/* 12 */            }
                L4: 
/* 13 */                wy[i] = true;

		            L6:
		                counter = i + 1;
                    do
                  		 	:: counter >= N -> break;
                        :: else ->
                            if
                                :: !(!we[counter] || wy[counter]) -> goto L6
                                :: else -> counter++;
                            fi;
		                od;
                    /* TODO: czekaj, az dla wszystkich k z [i+1..N-1] zachodzi !we[k] || wy[k] */

		            L7:
                    counter = 0;
		                do
              		    	:: counter >= i -> break;
                        :: else ->
                            if
                                :: we[counter] -> goto L7
                                :: else -> counter++;
                            fi;
                    od;
                    /* TODO: czekaj, az dla wszystkich k z [0..i-1] zachodzi !we[k] */
                sk:
                    csk++;    
                    counter = 0;
                    do
                        :: counter >= N -> break;
                        :: else -> 
                            if
                              :: prolog[counter] -> { sk_counter[counter]++; counter++; }
                              :: else -> counter++;
                            fi;
                    od; 

                    sk_counter[i] = 0;
                    prolog[i] = false;
                    /* SEKCJA KRYTYCZNA */
                    csk--;

/* 14 */            wy[i] = false; 
                          

/* 15 */            we[i] = false;
/* 16 */            chce[i] = false;

/* 17 */            goto start
/* 18 */        }

ltl wzajemne_wykluczanie { [] ( csk < 2 )}
ltl nieunikniona_poczekalnia { []( P[0]@sk -> was_pocz[0]) } /* poczekalania rownowazna sekcji krytycznej */
ltl wyjscie_z_poczekalni { [] ((we[0] && !chce[0])-> <>(wy[1] || wy[2] || wy[3])) }
ltl brak_zaglodzenia { [](P[0]@prot -> <>P[0]@sk )} 
ltl liniowosc { [](prolog[0] -> sk_counter[0] <= 2 * N)}