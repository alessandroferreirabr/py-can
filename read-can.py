import can
import os
import csv
from datetime import datetime

def save_can_message_to_csv(message, log_filename="can_log.csv"):
    # Define se o cabeçalho deve ser escrito
    write_header = not os.path.exists(log_filename)

    # Define os dados no CSV
    fieldnames = ['timestamp', 'arbitration_id', 'data', 'dlc', 'is_extended_id']

    # Abre o arquivo em modo de adição (append), cria se não existir
    with open(log_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escreve o cabeçalho se for o caso
        if write_header:
            writer.writeheader()

        # Escreve uma linha de log
        writer.writerow({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'arbitration_id': hex(message.arbitration_id),
            'data': ' '.join(f'{b:02X}' for b in message.data),
            'dlc': message.dlc,
            'is_extended_id': message.is_extended_id
        })
with can.Bus(interface='pcan',channel='PCAN_USBBUS1',bitrate=250000) as bus:
    
    for msg in bus:
        print(msg)
        save_can_message_to_csv(msg)