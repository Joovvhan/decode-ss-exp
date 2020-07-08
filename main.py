from glob import glob
from collections import namedtuple

import json
import csv

OptitrackRecord = namedtuple('optitrack_record', ('id', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz'))

ZigRecord = namedtuple('zig_record', ('id', 'x', 'y', 'z', 'yaw', 'pitch', 'distance'))

def organize_opti_record(data_as_list):
    
    assert len(data_as_list) == 25, f'Length of Optitrack Record is Not 25, {len(data_as_list)}'
    
    button_pushed = bool(int(float(data_as_list[0])))
    
    zig_id = int(float(data_as_list[1]))
    zig_position = data_as_list[2:5]
    zig_quaternion = data_as_list[5:9]
    
    p1_id = int(float(data_as_list[9]))
    p1_position = data_as_list[10:13]
    p1_quaternion = data_as_list[13:17]
    
    p2_id = int(float(data_as_list[17]))
    p2_position = data_as_list[18:21]
    p2_quaternion = data_as_list[21:25]
    
    zig_opti_record = OptitrackRecord(zig_id, *zig_position, *zig_quaternion)
    p1_opti_record = OptitrackRecord(p1_id, *p1_position, *p1_quaternion)
    p2_opti_record = OptitrackRecord(p2_id, *p2_position, *p2_quaternion)
    
    return button_pushed, zig_opti_record, p1_opti_record, p2_opti_record
    
    
def organize_zig_record(data_as_dict_list):
    
    current_time = data_as_dict_list[0]['current_time']
    
    person_info_list = list()
    for person_info in data_as_dict_list[1:]:
        person_zig_record = ZigRecord(person_info['id'], 
                                      *person_info['position_head'],
                                      *person_info["yaw/pitch"],
                                      person_info["r_distance"],
                                     )
        person_info_list.append(person_zig_record)
    
    return current_time, person_info_list

def main():

    experiment_files = [file for file in glob('*.txt') if 'exp' in file]
    
    experiment_file = experiment_files[0]
    
    csv_file_name = experiment_file.replace('.txt', '.csv')
    
    recording_start_time = None

    with open(csv_file_name, 'w') as csv_file:

        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['Current Time', 'Relative Time', 'Button Pushed',
                            'Zig ID', 'Zig X', 'Zig Y', 'Zig Z', 
                            'Zig Qw', 'Zig Qx', 'Zig Qy', 'Zig Qz',
                            'P1 ID', 'P1 X', 'P1 Y', 'P1 Z', 
                            'P1 Qw', 'P1 Qx', 'P1 Qy', 'P1 Qz',
                            'P2 ID', 'P2 X', 'P2 Y', 'P2 Z', 
                            'P2 Qw', 'P2 Qx', 'P2 Qy', 'P2 Qz',
                            'Zig 1 ID', 'Zig 1 X', 'Zig 1 Y', 'Zig 1 Z', 
                            'Zig 1 Yaw', 'Zig 1 Pitch', 'Zig 1 Distance',
                            'Zig 2 ID', 'Zig 2 X', 'Zig 2 Y', 'Zig 2 Z', 
                            'Zig 2 Yaw', 'Zig 2 Pitch', 'Zig 2 Distance',
                            ])

        with open(experiment_file, 'r') as f:
            for i, line in enumerate(f):

                split_index = line.rfind(']') + 1

                optitrack_record = line[split_index:].strip().split('\t')

                button_pushed, zig_opti_record, p1_opti_record, p2_opti_record = organize_opti_record(optitrack_record)

                zig_text = line[:split_index]
                zig_record = json.loads(zig_text)

                current_time, zig_person_info_list = organize_zig_record(zig_record)

                if i == 0:
                    recording_start_time = current_time

                relative_time = current_time - recording_start_time

                csv_record = [current_time, relative_time, button_pushed]

                csv_record.extend([*zig_opti_record])
                csv_record.extend([*p1_opti_record])
                csv_record.extend([*p2_opti_record])

                for zig_person_info in zig_person_info_list:
                    csv_record.extend([*zig_person_info])

                if '*' not in zig_text: 
                    csv_writer.writerow(csv_record)
                else:
                    csv_writer.writerow(zig_text)

if __name__ == '__main__':
    main()
            
            
    
    