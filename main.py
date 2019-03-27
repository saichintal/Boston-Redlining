import json


CODE_TRANSLATOR = { 'D':"Dangerous",
                    'C':'Definitely Declining',
                    'B':'Still Desireable',
                    'A':'Best'}

ZIPCODER_REDLINE = {'02108':{'NA': 0.9 ,'C': 0.5, 'B': 0.5},
                    '02109':{'NA': 1}, 
                    '02110':{'NA': 1},
                    '02111':{'D': 0.5, 'NA':0.5},
                    '02113':{'D': 1},
                    '02114':{'D': 0.95,'C':0.5 }, 
                    '02115':{'C': 0.5,'D': 0.5},
                    '02116':{'D': 0.6,'C': 0.2 ,'B': 0.2}, 
                    '02118':{'D': 1},
                    '02119':{'D': 1},
                    '02120':{'D': 1},
                    '02121':{'C': 1},
                    '02122':{'D': 0.75 ,'C': 0.25}, 
                    '02124':{'C': 0.9,'B': 0.1},
                    '02125':{'C': 0.9,'D': 0.1}, 
                    '02126':{'C': 0.9,'B': 0.1},
                    '02127':{'NA': 0.5, 'C': 0.25, 'D': 0.25},
                    '02128':{'NA':.6,'D':0.2,'C':0.15, 'B':0.5},
                    '02129':{'D': 0.6, 'NA': 0.4 },
                    '02130':{'A':0.15, 'B':0.1,'C': 0.75},
                    '02131':{'C':1},
                    '02132':{'C':0.6,'B':0.4},
                    '02134':{'NA':0.3,'D':0.4,'C':0.3},
                    '02135':{'B':0.1,'C':0.4,'D':0.5},
                    '02136':{'C':1},
                    '02151':{'D':0.5,'C':0.5},
                    '02152':{'B':.4, 'C':0.5, 'D':0.1},
                    '02163':{'NA':1},
                    '02199':{'NA':1},
                    '02203':{'NA':1},
                    '02210':{'NA':1},
                    '02215':{'C':0.9,'B':0.1},
                    '02467':{'A':0.9,'B':0.1}
                    }

NEIGHBORHOODS = { 'ALLSTON':'02134',
		 'BACKBAY':'02116',
		 'BAYVILLAGE':'02116',
		 'BEACONHILL':'02108',
		 'BRIGHTON':'02135',
		 'CHARLESTOWN':'02129',
		 'CHINATOWNLEATHERDISTRICT':'02111',
		 'DORCHESTER':['02121','02122','02124','02125'],
		 'DOWNTOWN':'02201',
		 'EASTBOSTON':'02128',
		 'LONGWOOD':'02115'
		 'FENWAYKENMORE':'02215', #the city of boston doesn't recognize longwood as it's own neighborhood and includes 02115 in fenway kenmore
		 'HYDEPARK':'02136',
		 'JAMAICAPLAIN' : '02130',
		 'MATTAPAN':'02126',
		 'MIDDORCHESTER':['02121','02122','02124','02125'],
		 'MISSIONHILL' : ['02120','02115'],
		 'NORTHEND':'02113',
		 'ROSLINDALE':'02131',
		 'ROXBURY':'02119',
		 'SOUTHBOSTON':'02127',
		 'SOUTHEND':'02118',
		 'WESTEND':'02114',
		 'WESTROXBURY':'02132'
                }

def load_data():
	

def main(): 


main() 
