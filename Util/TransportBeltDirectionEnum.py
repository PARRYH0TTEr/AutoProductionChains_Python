

class TransportBeltDirectionEnum:
    
    @staticmethod
    def GetDirection(direction_string):
        match direction_string:
            case "up":
                return 0
            
            case "down":
                return 4
            
            case "right":
                return 2
            
            case "left":
                return 6