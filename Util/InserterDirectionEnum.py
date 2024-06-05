

class InserterDirectionEnum:
    
    @staticmethod
    def GetDirection(direction_string):
        match direction_string:
            case "up":
                return 4
            
            case "down":
                return 0
            
            case "right":
                return 6
            
            case "left":
                return 2