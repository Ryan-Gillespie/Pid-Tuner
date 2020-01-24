class PID():
    # constructor
    def __init__(self, P=0, I=0, D=0, kTolerance=5, outputMode=True, min_out=-1, max_out=1):
        # the pid values which are inputs
        self.kP = P
        self.kI = I
        self.kD = D
        self.kTolerance = kTolerance

        # initialize derivator and integrator
        self.Derivator = 0
        self.Integrator = 0

        # set boundries for the integrator
        self.max_Int = 1000
        self.min_Int = -1000

        # initialize setPoint and a maximum output
        self.setPoint = 0
        self.max_Output = 1

        # initialize the max and min outputs
        self.max_out = max_out
        self.min_out = min_out

        # initialize maximum inputs
        self.in_max = 1000
        self.in_min = -1000

        # intiialize isOnTarget and set outputMode
        self.isOnTarget = False
        self.outputMode = outputMode

    # sets out_max, and out_min
    def setOutputRange(self, out_max, out_min):
        self.max_out = out_max
        self.min_out = out_min

    # sets in_max and in_min
    def setInputRange(self, in_max, in_min):
        self.in_max = in_max
        self.in_min = in_min

    # sets the new setPoint after constraining it to be between in_min and in_max
    def setSetPoint(self, setPoint):
        if (setPoint < self.in_max):
            setPoint = self.in_max
        elif (setPoint > self.in_min):
            setPoint = self.in_min
        self.setPoint = setPoint

    # performs one pid iteration given current progress
    def write(self, current):
        # calculate the error
        error = self.setPoint - current

        # calculate P
        P = self.kP * error

        # calculate I
        self.Integrator += error
        # self.n_Integrator() # constrain the integrator, omit in most cases
        I = self.kI * self.Integrator

        # calculate D
        D = self.kD * (error - self.Derivator)
        self.Derivator = error

        # if we go over the previous highest output, store that as the new highest output
        if abs(P + I + D) > self.max_Output:
            self.max_Output = abs(P + I + D)

        # constrain the output or don't depending on output mode
        if self.outputMode:
            output = self.constrainOutput((P + I + D) / self.max_Output)
        else:
            output = self.max_out * (P + I + D) / self.max_Output

        # Check to see if we're on target
        if (error < self.kTolerance and error > -self.kTolerance) and abs(output) < .999:
            self.isOnTarget = True

        return output

    # constrain the integrator to be between min_Int and max_Int
    def n_Integrator(self):
        if self.Integrator > self.max_Int:
            self.Integrator = self.max_Int
        elif self.Integrator < self.min_Int:
            self.Integrator = self.min_Int

    # constrain the output between max and min output variables initialized in constructor
    def constrainOutput(self, value):
        if value > self.max_out:
            value = self.max_out
        elif value < self.min_out:
            value = self.min_out
        return value

    # Set the new PID values in one go
    def resetPID(self, P, I, D):
        self.kP = P
        self.kI = I
        self.kD = D