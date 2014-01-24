import sys
import os
import subprocess
import time


class Lvm:
    """Wrap LVM programs."""
    
    def vgdisplay(self, vg_name):
        """
        1  vg_name          volume group name
        2  vg_access        volume group access
        3  vg_status        volume group status
        4  vg_num           internal volume group number
        5  vg_max_lv        maximum number of logical volumes
        6  vg_current_lv    current number of logical volumes
        7  vg_open_lv       open count of all logical volumes in this volume group
        8  vg_max_lvsize    maximum logical volume size
        9  vg_max_pv        maximum number of physical volumes
        10 vg_current_pv    current number of physical volumes
        11 vg_actual_pv     actual number of physical volumes
        12 vg_size          size of volume group in kilobytes
        13 vg_extent_size   physical extent size
        14 vg_total_extents total number of physical extents for this volume group
        15 vg_alloc_extents allocated number of physical extents for this volume group
        16 vg_free_extents  free number of physical extents for this volume group
        17 vg_uuid          uuid of volume group
        
        Return dict of vgdisplay information
        """
        call = ['/sbin/vgdisplay', '-c', vg_name]
        proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        
        if err:
            print err
            #~ sys.exit(1)
            
        out_list = out.rstrip().split(':')

        vginfo = {
            'vg_name':          out_list[0],
            'vg_access':        out_list[1],
            'vg_status':        out_list[2],
            'vg_num':           out_list[3],
            'vg_max_lv':        out_list[4],
            'vg_current_lv':    out_list[5],
            'vg_open_lv':       out_list[6],
            'vg_max_lvsize':    out_list[7],
            'vg_max_pv':        out_list[8],
            'vg_current_pv':    out_list[9],
            'vg_actual_pv':     out_list[10],
            'vg_size':          out_list[11],
            'vg_extent_size':   out_list[12],
            'vg_total_extents': out_list[13],
            'vg_alloc_extents': out_list[14],
            'vg_free_extents':  out_list[15],
            'vg_uuid':          out_list[16]
        }

        return vginfo
        
    def lvcreate_snapshot(self, vg_path, lv_name, size):
        """Create a snapshot of a logical volume
        
        return snapshot_name or None
        """
        timestamp = str(int(time.time()))
        lv_path = os.path.join(vg_path, lv_name)
        snapshot_name = '{0}--snapshot-{1}'.format(lv_name, timestamp)

        call = ['/sbin/lvcreate', '--size', size, '--snapshot', '--name', snapshot_name, lv_path]
        proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        returncode = proc.returncode
        
        if err:
            print err
            #~ sys.exit(1)
        
        if returncode != 0:
            return None
        return snapshot_name
        
lvm = Lvm()
print lvm.vgdisplay("test-vg")
lvm.lvcreate_snapshot('/dev/test-vg', 'test-lv', '5M')
