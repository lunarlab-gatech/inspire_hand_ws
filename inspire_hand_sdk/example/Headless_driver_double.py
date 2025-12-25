import multiprocessing
import time
from inspire_sdkpy import inspire_sdk, inspire_hand_defaut

def worker(ip,LR,name,network=None):
    handler=inspire_sdk.ModbusDataHandler(network=network,ip=ip, LR=LR, device_id=1)

    call_count = 0
    start_time = time.perf_counter()
    time.sleep(0.5)
    
    try:
        while True:
            data_dict = handler.read()
            call_count += 1
            time.sleep(0.001)
            
            if call_count % 10 == 0:
                elapsed_time = time.perf_counter() - start_time
                frequency = call_count / elapsed_time
                print(f"{name} Current Frequency: {frequency:.2f} Hz, Call Count: {call_count}, Elapsed Time: {elapsed_time:.6f} seconds")
    except KeyboardInterrupt:
        elapsed_time = time.perf_counter() - start_time
        frequency = call_count / elapsed_time if elapsed_time > 0 else 0
        print(f"{name} Program Ended. Total Call Count: {call_count}, Total Elapsed Time: {elapsed_time:.6f} seconds, Final Frequency: {frequency:.2f} Hz")

if __name__ == "__main__":
    # Example with default IP addresses

    process_r = multiprocessing.Process(target=worker, args=('192.168.123.211', 'r', "Right Hand Process"))
    process_l = multiprocessing.Process(target=worker, args=('192.168.123.210', 'l', "Left  Hand Process"))

    process_r.start()
    time.sleep(0.6)
    process_l.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        process_r.terminate()
        process_l.terminate()
