# """
# Open and close time calculations
# for ACP-sanctioned brevets
# following rules described at https://rusa.org/octime_acp.html
# and https://rusa.org/pages/rulesForRiders
# Name: Ethan Robb
# """
import arrow

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    distances = [
    {'start_dist': 0, 'end_dist': 200, 'max_speed': 34, 'min_speed': 15},
    {'start_dist': 200, 'end_dist': 400, 'max_speed': 32, 'min_speed': 15},
    {'start_dist': 400, 'end_dist': 600, 'max_speed': 30, 'min_speed': 15},
    {'start_dist': 600, 'end_dist': 1000, 'max_speed': 28, 'min_speed': 11.428}]
   
    #Input Error Checkpoint
    if control_dist_km < 0: #Negative value check
        raise ValueError
    elif control_dist_km == 0: #If control distance is 0
        return brevet_start_time
    elif control_dist_km > int(brevet_dist_km):
        control_dist_km = int(brevet_dist_km)

    min_shift = 0
    log = ""
    control_open_time = brevet_start_time

    for dist_span in distances:
        if dist_span['start_dist'] < control_dist_km <= dist_span['end_dist']:
            log += "entering if with control_open_time = {}".format(control_open_time)
            fastest = (control_dist_km - dist_span['start_dist']) / dist_span['max_speed']
            min_shift += fastest * 60
            break
        else:
            log += "entering else with control_open_time = {}".format(control_open_time)
            added = (dist_span['end_dist'] - dist_span['start_dist']) / dist_span['max_speed']
            min_shift += added * 60
            log += "exiting else with control_open_time = {}".format(control_open_time)
    
    control_open_time = control_open_time.shift(minutes=+round(min_shift))
    return control_open_time
    
def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    distances = [
    {'start_dist': 0, 'end_dist': 200, 'max_speed': 34, 'min_speed': 15},
    {'start_dist': 200, 'end_dist': 400, 'max_speed': 32, 'min_speed': 15},
    {'start_dist': 400, 'end_dist': 600, 'max_speed': 30, 'min_speed': 15},
    {'start_dist': 600, 'end_dist': 1000, 'max_speed': 28, 'min_speed': 11.428}]

    #input error checkpoint
    if control_dist_km < 0: #Negative Value Check
        raise ValueError
    elif control_dist_km == 0: #If control distance is 0
        return brevet_start_time.shift(minutes=+60)
    elif control_dist_km <= 60: 
        minute_shift = round((control_dist_km/20) * 60 + 60)
        return brevet_start_time.shift(minutes=+minute_shift)
    elif control_dist_km >= int(brevet_dist_km):
        control_dist_km = int(brevet_dist_km)

    control_close_time = brevet_start_time
    minute_shift = 0

    for dist_span in distances:
        if dist_span['start_dist'] < control_dist_km <= dist_span['end_dist']:
            slowest = (control_dist_km - dist_span['start_dist']) / dist_span['min_speed']

            minute_shift += slowest * 60
            break
        else:
            added = (dist_span['end_dist'] - dist_span['start_dist']) / dist_span['min_speed']
            minute_shift += added * 60
        
    control_close_time = control_close_time.shift(minutes=+round(minute_shift))
    return control_close_time
