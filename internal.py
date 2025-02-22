import os
import threading

def count_files_by_extension( path, extension ):
    drivers_count = 0
    try:
        for file in os.listdir( path ):
            if os.path.isdir( "\\".join( ( path, file ) ) ):
                drivers_count += count_files_by_extension( "\\".join( ( path, file ) ), extension )
            
            if file.endswith( extension ):
                drivers_count += 1
            
    except PermissionError:
        pass

    return drivers_count
        
def iterate_all_drivers_in_path( path, iterate_function ):
    threads_list = []
    try:
        for file in os.listdir( path ):
            if os.path.isdir( "\\".join( ( path, file ) ) ):
                threads_list += iterate_all_drivers_in_path( "\\".join( ( path, file ) ), iterate_function )
            if file.endswith( ".sys" ):
                thread = threading.Thread( target=iterate_function, args=( path, file ) )
                threads_list.append( thread )
                thread.start()
    except PermissionError:
        pass

    return threads_list
