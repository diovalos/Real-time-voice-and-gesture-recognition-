ECHO OFF
ECHO enter 1 for hand gesture 
ECHO enter 2 for head gesture
ECHO enter 3 for speech recognition
SET /p environment="enter choice: "
IF /i "%environment%" == "1" GOTO live
IF /i "%environment%" == "2" GOTO dev
IF /i "%environment%" == "3" GOTO pop

ECHO Invalid Option
GOTO end

:live
ECHO option selection : hand gesture recognition
python "D:\kalej\MooN\college\_SEM6\wireless\projo\finals\hand.py" %*
goto end

:dev
ECHO option selection : head tilt recognition
python "D:\kalej\MooN\college\_SEM6\wireless\projo\finals\head_tilt.py" %*
goto end

:pop
ECHO option selection : speech recognition
python "D:\kalej\MooN\college\_SEM6\wireless\projo\finals\voice.py" %*
goto end
:end
PAUSE