import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import mimetypes

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            # Verificar el tipo MIME del archivo
            mime_type, _ = mimetypes.guess_type(filename)
            
            # Definir carpetas de destino
            jpg_destination_folder = "C:/Users/maxvi/Desktop/NOVES DESCARGUES JPG"
            pdf_destination_folder = "C:/Users/maxvi/Desktop/NOVES DESCARGUES PDF"
            
            # Determinar la carpeta de destino en función del tipo MIME
            if mime_type == 'image/jpeg':
                destination_folder = jpg_destination_folder
            elif mime_type == 'application/pdf':
                destination_folder = pdf_destination_folder
            else:
                # Si no es ni JPG ni PDF, no hacer nada
                return

            retries = 5  # Número de intentos de reintento
            delay = 2    # Esperar 2 segundos entre intentos

            for _ in range(retries):
                if os.path.exists(filename):
                    try:
                        shutil.move(filename, destination_folder)
                        print(f"Archivo {os.path.basename(filename)} movido a {destination_folder}")
                        break
                    except PermissionError as e:
                        print(f"No se pudo mover el archivo {filename}: {e}")
                        time.sleep(delay)  # Esperar antes de reintentar
                    except Exception as e:
                        print(f"Error al mover el archivo {filename}: {e}")
                        break
                else:
                    print(f"Archivo {filename} no encontrado. Reintentando en {delay} segundos...")
                    time.sleep(delay)
            else:
                print(f"No se pudo mover el archivo {filename} después de varios intentos.")

def main():
    folder_to_watch = "C:/Users/maxvi/Downloads"  # Ruta de la carpeta a monitorear
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Esperar 1 segundo en cada iteración del bucle principal
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
