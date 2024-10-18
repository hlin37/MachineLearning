## Takes in HTML from Element Console: <div class = "play-by-play"></div>

import re

gameEventRealTime = []

with open('gamedata.txt') as f:

    firstGameDistances = []
    firstGameEvents = []

    secondGameDistances = []
    secondGameEvents = []

    lines = f.readlines()

    home = 0
    for line in lines:

        distanceArray = None
        eventArray = None
        if home % 2 == 0:
            distanceArray = firstGameDistances
            eventArray = firstGameEvents
        else:
            distanceArray = secondGameDistances
            eventArray = secondGameEvents

        quarter = 0
        quarters = [i.start() for i in re.finditer('h3 class="play-by-play-quarter-header">', line)]

        distances = [i.start() for i in re.finditer('<div class="play-by-play-event-distance">', line)]
        for distance in distances:
            if (quarter < len(quarters)):
                if quarters[quarter] < distance:
                    distanceArray.append("QUARTER")
                    quarter += 1
            result = line[distance + 41 : distance + 45]
            resultIntegers = re.findall(r'\d+', result)
            if (len(resultIntegers) == 0):
                distanceArray.append(0)
            else:
                distanceArray.append(int(resultIntegers[0]))

        quarter = 0

        events = [i.start() for i in re.finditer('<div class="play-by-play-event-label">', line)]
        index = 0
        for event in events:
            if (quarter < len(quarters)):
                if quarters[quarter] < event:
                    eventArray.append("QUARTER")
                    quarter += 1
                
            while (line[event + 38 + index] != "<"):
                index += 1
        
            eventArray.append(line[event + 38 : event + 38 + index])

            index = 0
    

        for i in range(len(eventArray)):
            if "They scored" in eventArray[i] or "Timeout" in eventArray[i] or "Injury" in eventArray[i] or "Throwaway caused" in eventArray[i]:
                distanceArray[i] = None
                eventArray[i] = None

        eventArray = [item for item in eventArray if item is not None]
        distanceArray = [item for item in distanceArray if item is not None]

        if home % 2 == 0:
            firstGameDistances = distanceArray
            firstGameEvents = eventArray
        else:
            secondGameDistances = distanceArray
            secondGameEvents = eventArray
        
        home += 1

        if (len(secondGameEvents) > 0):
            firstCounter = 0
            secondCounter = 0
            iterateDistance = None
            iterateEvent = None
            iterateCounter = None

            firstTeamPull = None
            secondTeamPull = None


            if "Pull" in firstGameEvents[firstCounter]:
                firstTeamPull = True
                
            else:
                secondTeamPull = True
       
            while (firstCounter < len(firstGameEvents) or secondCounter < len(secondGameEvents)):

                if (firstCounter > len(firstGameEvents)):
                    print("here1")

                if "QUARTER" in firstGameEvents[firstCounter] and "QUARTER" in secondGameEvents[secondCounter]:
                    firstCounter += 1
                    secondCounter += 1

                if "Pull" in firstGameEvents[firstCounter]:
                    result = str(firstGameDistances[firstCounter]) + " " + firstGameEvents[firstCounter]
                    firstCounter += 1
                    gameEventRealTime.append(result)
                    iterateDistance = secondGameDistances
                    iterateEvent = secondGameEvents
                    iterateCounter = secondCounter
                    firstTeamPull = False
               
    
                elif "Pull" in secondGameEvents[secondCounter]:
                    result = str(secondGameDistances[secondCounter]) + " " + secondGameEvents[secondCounter]
                    secondCounter += 1
                    gameEventRealTime.append(result)
                    iterateDistance = firstGameDistances
                    iterateEvent = firstGameEvents
                    iterateCounter = firstCounter
                    secondTeamPull = False
                    
                else:
                    print("here")
                
                while "Score" not in iterateEvent[iterateCounter]:
                    
                    if "Throwaway caused" in iterateEvent[iterateCounter]:
                        iterateCounter += 1
                    elif "Swing" in iterateEvent[iterateCounter] or "Pass" in iterateEvent[iterateCounter] or "Dump" in iterateEvent[iterateCounter] or "Dish" in iterateEvent[iterateCounter] or "Block" in iterateEvent[iterateCounter] or "Huck from" in iterateEvent[iterateCounter]:
                        result = str(iterateDistance[iterateCounter]) + " " + iterateEvent[iterateCounter]
                        gameEventRealTime.append(result)
                        iterateCounter += 1
                    elif "Dropped" in iterateEvent[iterateCounter] or "Huck throwaway" in iterateEvent[iterateCounter] or "Throwaway" in iterateEvent[iterateCounter] or "Stall" in iterateEvent[iterateCounter]:
                        result = str(iterateDistance[iterateCounter]) + " " + iterateEvent[iterateCounter]
                        gameEventRealTime.append(result)
                        iterateCounter += 1

                        ## I need to switch games because there was a turnover
                        if (iterateDistance == firstGameDistances):
                            iterateDistance = secondGameDistances
                            iterateEvent = secondGameEvents
                            firstCounter = iterateCounter
                            iterateCounter = secondCounter
                        else:
                            iterateDistance = firstGameDistances
                            iterateEvent = firstGameEvents
                            secondCounter = iterateCounter
                            iterateCounter = firstCounter
                    else:
                        result = str(iterateDistance[iterateCounter]) + " " + iterateEvent[iterateCounter]
                        if "QUARTER QUARTER" in result:
                            if (iterateEvent == firstGameEvents):
                                firstCounter = iterateCounter
                                
                            else:
                                secondCounter = iterateCounter
                            break   
                        print(result)
                        iterateCounter += 1
                    
                    if (iterateCounter >= len(iterateEvent)):
                        if (iterateDistance == firstGameDistances):
                            firstCounter = iterateCounter
                        else:
                            secondCounter = iterateCounter
                        break
                
                if (iterateCounter >= len(iterateEvent)):
                    if (iterateDistance == firstGameDistances):
                        firstCounter = iterateCounter
                    else:
                        secondCounter = iterateCounter
                    break

                if "Score" in iterateEvent[iterateCounter]:
                    result = str(iterateDistance[iterateCounter]) + " " + iterateEvent[iterateCounter]
                    gameEventRealTime.append(result)
                    iterateCounter += 1 

                    if (iterateDistance == firstGameDistances):
                        # iterateDistance = secondGameDistances
                        # iterateEvent = secondGameEvents
                        firstCounter = iterateCounter
                        firstTeamPull = True
                    else:
                        # iterateDistance = firstGameDistances
                        # iterateEvent = firstGameEvents
                        secondCounter = iterateCounter
                        secondTeamPull = True


            print(gameEventRealTime)
            # g = open("gameEvent.txt", "a")
            # for gameEvent in gameEventRealTime:
            #     g.write(gameEvent)
            #     g.write("\n")
            
            firstGameDistances = []
            firstGameEvents = []

            secondGameDistances = []
            secondGameEvents = []

            gameEventRealTime = []

            # g.write("------------------------------------------")
            # g.write("\n")

f.close()