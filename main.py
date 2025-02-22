import os
import sys
import time
import internal
import threading
import progressbar
from driver_class import Driver

cwd = os.path.dirname( sys.executable ) if hasattr( sys, "frozen" ) else os.path.dirname( os.path.realpath( sys.argv[ 0 ] ) )
main_thread = threading.current_thread( )
suspect_functions = [ "MmMapIoSpace", "MmUnmapIoSpace", "MmGetPhysicalAddress",
                    "ZwMapViewOfSection", "MmGetSystemRoutineAddress", "MmMapIoSpaceEx"]

def get_driver_info_callback( path, file ):
    thread = threading.current_thread( )

    driver = Driver( path, file )
    if not driver.have_device:
        setattr( thread, "driver", False )
        return

    for func in suspect_functions:
        if not func in driver.content:
            continue
        driver.increase_severity( 1 )

    setattr( thread, "driver", driver )
    return

os.system( "title Possible Vulnerable Driver Tracker" )
os.system( "cls" )

print( "Possible Vulnerable Driver Tracker\n\t\tBy M47Z\n" )

search_dir = os.path.abspath( input( "Directory To Search: " ).lower( ).replace( "system32", "sysnative" ).replace( "syswow64", "system32" ) )

os.system( "cls" )

with progressbar.ProgressBar( max_value=internal.count_files_by_extension( search_dir, ".sys" ) ) as bar:
    print( "[+] Searching For All Possible Vulnerable Drivers\n" )

    setattr( main_thread, "progress", 0 )
    setattr( main_thread, "bar", bar )

    threads_list = internal.iterate_all_drivers_in_path( search_dir, get_driver_info_callback )

    drivers_list = [ ]
    for thread in threads_list:
        while getattr( thread, "driver", None ) == None:
            time.sleep( 0.025 )

        if getattr( thread, "driver", None ) != False:
            drivers_list.append( getattr( thread, "driver", None ) )
        
        setattr( main_thread, "progress", getattr( main_thread, "progress", 0 ) + 1 )
        getattr( main_thread, "bar", None ).update( getattr( main_thread, "progress", 0 ) )

if not os.path.isdir( "\\".join( ( cwd, "result" ) ) ):
    os.mkdir( "\\".join( ( cwd, "result" ) ) )

for file in os.listdir( "\\".join( ( cwd, "result" ) ) ):
    os.remove( "\\".join( ( cwd, "result", file ) ) )

for i in range( 1, len( suspect_functions ) + 1 ):
    filtered_drivers_list = list( filter( lambda driver: driver.severity == i, drivers_list ) )
    if not len( filtered_drivers_list ) > 0:
        continue

    file = open( "\\".join( ( cwd, "result", ".".join( ( str(i), "txt" ) ) ) ), "w" )
    for driver in filtered_drivers_list:
        driver_path = ( "" if driver.path[ len( driver.path ) - 1: ] == "\\" else "\\" ).join( ( driver.path, driver.name ) )
        driver_path = driver_path.replace( "system32", "syswow64" ).replace( "sysnative", "system32" )
        file.write( "{}\n".format( driver_path ) )
    file.close( )

print( "\n\nPress Any Key to Exit" )
os.system( "pause>nul" )
