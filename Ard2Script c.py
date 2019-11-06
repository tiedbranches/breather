
import serial
from numpy import array
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


ser = serial.Serial('/dev/cu.usbmodem14301', 9600) # Establish the connection on a specific port

readinglist=[]
plotlist=[]
gradientpoints=[]
gradientlist=[0]
g=0
grplotlist=[0]
correctedlist=[]

index=0
lasti=0
firstcycle=False
runon=False

gradientscope=20



# main loop reading voltages from breather
for i in range(0,5000):

    fanread=ser.readline()
    bfanread=int(fanread.decode('utf-8'))+300
    print(bfanread)
    readinglist.append(bfanread)

    plotlist.append(i)
    i+=1


    # Initial buffer of 600.
    if i>600:

        # Has there been a gradient change?
        if gradientlist[-1] != gradientlist[-2]:

            # Are we currently in a run?
            if runon==True:

                # We're in a run and there has been a gradient change. Is it a new one or a bouncer?
                # A new one.
                if (i-lasti)>gradientscope:

                    lasti=i #It's a valid gradient change. Still don't know cycle.

                    # It's a new gradient change. If this is ending first cycle then we need to switch firstcycle.
                    if firstcycle==True:

                        correctedlist.append(index-(bfanread-index))
                        print("Printer A at i:",i)
                        # End of first cycle. (b)
                        firstcycle=False
                        print("FIRSTCYCLE turned OFF at i:",i)

                    # It's a new gradient change and we're not in a firstcycle. Hence this has to be the end.
                    # Of both second cycle and run.
                    else:
                        correctedlist.append(bfanread)
                        print("Printer B at i:",i)

                        firstcycle=True
                        print("FIRSTCYCLE turned ON at i:",i)
                        runon=False # <<<<<OFF SWITCH
                        print("RUNON switched RUN OFF at i:",i)


                # A bouncer.
                else:
                    correctedlist.append(index-(bfanread-index))
                    print("Printer C at i:",i)

            # We're not in a run.
            else:

                # Not in a run, but there has been a gradient change. Is it a new one or a bouncer?
                if (i-lasti)>gradientscope:

                    lasti=i # It's a valid gradient change.

                    # It's a new one. If we're in the off-run's 2nd cycle we will need to switch the run-state.
                    # This happens down in else. Now we are in firstcycle, but ending it.
                    if firstcycle==True:

                        correctedlist.append(bfanread)
                        print("Printer D at i:",i)
                        # Switch firstcycle off since we're necessarily entering second cycle. (d)
                        firstcycle=False
                        print("FIRSTCYCLE turned OFF at i:",i)

                    # It's the second cycle and we're not in a run. Time to switch the run-state.
                    # Run starts, and an index is made.
                    else:
                        index=readinglist[-1]
                        # Should be about the same, but I guess it's like starting one step behind, which suits us.
                        correctedlist.append(index-(bfanread-index))
                        print("Printer E at i:",i)

                        runon=True # <<<<<<<ON SWITCH
                        print("RUNON turned RUN ON at i:",i)
                        firstcycle=True
                        print("FIRSTCYCLE turned ON at:",i)

                # It's a bouncer.
                else:

                    # Not a new one so no chance to trigger a run-state change.
                    correctedlist.append(bfanread)
                    print("Printer F at i:",i)


        else:

            # Are we currently in a run?
            # This should be the large majority of readings. No gradient change, but inside a run.
            if runon==True:

                correctedlist.append(index-(bfanread-index))
                print("Printer G at i:",i)

            # And these are the points after threshold, but outside a run. Also a large bunch.
            else:

                correctedlist.append(bfanread)
                print("Printer H at i:",i)

    # All points in correctedlist before the threshold.
    else:

        correctedlist.append(bfanread)
        print("Printer Y at i:",i)


    # gradient detector
    if i%gradientscope==0:
        gradientpoints.append(bfanread)


        if g != 0:
            gradient=gradientpoints[g]-gradientpoints[g-1]
            grplotlist.append(i)

            if gradient<=0:
                gradientlist.append(-100)
                print("NEGATIVE GRADIENT")

            else:
                gradientlist.append(100)
                print("POSITIVE GRADIENT")

        g += 1


y=array(readinglist)

x=array(plotlist)

yhat=savgol_filter(y,15,7)

gr=array(gradientlist)

xhat=array(grplotlist)

corrected=array(correctedlist)



plt.figure(figsize=(31,3))
plt.plot(x,y)
plt.plot(x,yhat, color='red')
plt.plot(xhat,gr, color="orange")
plt.plot(x,corrected,color="green")

plt.show()




