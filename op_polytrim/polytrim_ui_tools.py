'''
Created on Oct 10, 2015

@author: Patrick
'''
from .. import common_utilities

class Polytrim_UI_Tools():
    
    def sketch_confirm(self, context, eventd):
        print('sketch confirmed')
        if len(self.sketch) < 5 and self.knife.ui_type == 'DENSE_POLY':
            print('sketch too short, cant confirm')
            return
        x,y = eventd['mouse']
        last_hovered = self.knife.hovered[1] #guaranteed to be a point by criteria to enter sketch mode
        self.knife.hover(context,x,y)
        print('last hovered %i' % last_hovered)
        
        sketch_3d = common_utilities.ray_cast_path(context, self.knife.cut_ob,self.sketch)
        
        if self.knife.hovered[0] == None:
            #add the points in
            if last_hovered == len(self.knife.pts) - 1:
                self.knife.pts += sketch_3d[0::5]
                print('add on to the tail')

                
            else:
                self.knife.pts = self.knife.pts[:last_hovered] + sketch_3d[0::5]
                print('snipped off and added on to the tail')
        
        else:
            print('inserted new segment')
            print('now hovered %i' % self.knife.hovered[1])
            new_pts = sketch_3d[0::5]
            if last_hovered > self.knife.hovered[1]:
                new_pts.reverse()
                self.knife.pts = self.knife.pts[:self.knife.hovered[1]] + new_pts + self.knife.pts[last_hovered:]
            else:
                self.knife.pts = self.knife.pts[:last_hovered] + new_pts + self.knife.pts[self.knife.hovered[1]:]
        self.knife.snap_poly_line()