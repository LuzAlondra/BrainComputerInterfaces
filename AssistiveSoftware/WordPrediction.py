#September 9th 2009

#Word Prediction Module

def Options(word,options):
    #Common words banks (dictionary)
    Dictionary = {'a':['about','after','again','air','all','along','also','an','and','another','any','are','around',\
                       'as','at','away','able','above','across','add','against','ago','almost','among','animal',\
                       'answer','alone','already','although','am','America','anything','area','age','ask','action',\
                       'addition','afraid','afternoon','ahead','amount','ancient','anyone','arm','according','act',\
                       'actually','Africa','alike','apart','ate','attention','alive','angry','army','average',\
                       'airplane','angle','Ann','apple','art','Atlantic','atmosphere','ability','agree','ants',\
                       'Asia','asleep','attack','activity','Alaska','appearance','''aren't''','article','Aunt',\
                       'automobile','avoid','account','allow','anywhere','attached','audience','available','aid',\
                       'aloud','Andy','anyway','arrow','aside','atomic','author','accept','accident','active',\
                       'additional','adjective','affect','Alice','alphabet','announced','anybody','April','arrange',\
                       'Australia','aware','aboard','accurate','actual','adventure','apartment','applied','appropriate',\
                       'arrive','atom','acres','adult','advice','arrangement','attempt','August','Autumn'],
                  'b':['back','be','because','been','before','below','between','both','but','by','became','become',\
                       'began','behind','being','better','black','best','body','book','boy','brought','ball',\
                       'beautiful','beginning','Bill','birds','blue','boat','bottom','box','bring','build','building',\
                       'built','baby','base','beside','bright','business','buy','bad','bear','beyond','bit','blood',\
                       'board','Bob','born','break','British','broken','brother','brown','busy','bank','basic',\
                       'beat','blow','bone','bread','bag','band','Billy','branch','breakfast','breath','broke','bus',\
                       'bar','barn','baseball','beauty','believed','bell','belong','beneath','bigger','bottle',\
                       'bowl','broad','balance','bat','battle','Ben','block','bow','brain','brave','bridge','basket',\
                       'birthday','balloon','bare','bark','begun','bent','biggest','bill','blank','blew','breathing',\
                       'butter','basis','bean','becoming','Betsy','bicycle','blanket','brush','buffalo','burn','burst',\
                       'bush','badly','bee','belt','bite','blind','bound','Bay','behavior','bend','bet','birth',\
                       'brass','breathe','brief','buried','border','breeze','brick'],
                  'c':['came','can','come','could','call','cannot','car','certain','change','children','city',\
                       'close','cold','country','course','cut','''can't''','care','carefully','carried','carry',\
                       'center','check','class','coming','common','complete','case','catch','caught','child','choose',\
                       'circle','clear','color','copy','correct','''couldn't''','capital','cat','cattle','cause',\
                       'century','chance','clean','clothes','coast','control','cool','corn','corner','cover','cross',\
                       'careful','chair','chief','christmas','church','cloth','cloud','column','compare','contain',\
                       'continued','cost','cotton','count','cabin','California','camp','captain','cell','cent',\
                       'certainly','changing','closer','coal','coat','community','company','completely','compound',\
                       'condition','consider','correctly','crop','crowd','current','chapter','chart','Chinese',\
                       'clearly','climate','clock','closely','clothing','coffee','cow','cry','cave','charge',\
                       'chemical','China','clay','climb','composition','congress','copper','crew','cup','cage','cake',\
                       'Canada','central','character','Charles','chicken','chosen','club','cook','court','cream',\
                       'cutting','cap','carbon','card','chain','cheese','chest','Chicago','choice','circus','citizen',\
                       'classroom','college','consist','continent','conversation','courage','cowboy','creature',\
                       'collect','colony','combination','combine','comfortable','complex','composed','concerned',\
                       'connected','construction','couple','create','curious','castle','characteristic','Columbus',\
                       'compass','consonant','curve','camera','captured','chamber','command','crack','calm','canal',\
                       'Casey','cast','chose','claws','coach','constantly','contrast','cookies','customs'],
                  'd':['day','did','different','do','does','''don't''','down','''didn't''','dog','done','door',\
                       'draw','during','dark','deep','distance','doing','dry','difference','direction','dried','Dan',\
                       'dead','deal','death','decide','difficult','''doesn't''','drive','dance','describe','desert',\
                       'dinner','doctor','dollar','drop','dropped','danger','dear','degree','develop','die',\
                       'directly','discover','divide','double','Dr.','dress','drink','drove','dust','Dad','dangerous',\
                       'deer','desk','detail','development','drew','driver','daughter','design','determine','direct',\
                       'discuss','division','drawn','daily','darkness','diagram','Dick','disappear','doubt','dozen',\
                       'dream','driving','date','depend','differ','discovery','disease','duck','due','Dutch','dig',\
                       'dirt','distant','dot','definition','dish','Don','driven','dug','Daniel','David','dawn',\
                       'declared','diameter','difficulty','dirty','dull','duty','damage','Danny','deeply','depth',\
                       'discussion','doll','donkey'],
                  'e':['each','end','even','every','early','earth','eat','enough','ever','example','eye','easy',\
                       'either','else','everyone','everything','easily','edge','egg','eight','energy','England',\
                       'especially','Europe','exactly','except','explain','engine','evening','ear','east','electric',\
                       'element','enjoy','equal','exercise','experiment','easier','effect','electricity','empty',\
                       'entire','everybody','exciting','expect','experience','express','event','everywhere','earlier',\
                       'eaten','education','enemy','enter','equipment','escape','European','excited','expression',\
                       'extra','effort','establish','exact','excitement','entirely','environment','exclaimed','Edward',\
                       'elephant','etc.','evidence','examine','excellent','earn','Eddy','eventually','explore','eager',\
                       'eleven','engineer','equally','equator','Egypt','Ellen','essential','exchange','exist',\
                       'explanation'], 
                  'f':['few','find','first','for','found','from','face','family','far','father','feel','feet',\
                       'fire','fish','five','food','form','four','front','fact','fall','fast','felt','field',\
                       'finally','fine','floor','follow','foot','friend','full','famous','farm','fell','figure',\
                       'flat','fly','forest','free','French','fun','farmer','faster','fight','fill','finger','force',\
                       'forward','France','fresh','familiar','farther','fear','forth','fair','feed','final','finish',\
                       'flew','fruit','further','future','fat','favorite','fence','fifty','flight','flow','flower',\
                       'forget','fourth','friendly','factory','feathers','fellow','fighting','fought','Frank',\
                       'freedom','funny','fur','fifteen','flag','flies','football','foreign','frame','frequently',\
                       'frighten','function','factor','fog','forgot','forgotten','frozen','fuel','furniture','failed',\
                       'fallen','fastened','feature','fed','fairly','fewer','fifth','Florida','fierce','firm','fix',\
                       'flame','former','forty','fox','Fred','frog','fully','facing','film','finest','fireplace',\
                       'floating','folks','fort'],
                  'g':['get','give','go','good','great','gave','given','got','green','ground','group','grow','game',\
                       'getting','girl','glass','goes','gold','gone','George','government','grass','grew','garden',\
                       'general','glad','greater','greatest','guess','gas','giving','gray','grown','Greek','guide',\
                       'gun','generally','German','Germany','giant','golden','grain','growth','gate','gently',\
                       'gradually','gather','gentle','globe','grandfather','greatly','gain','graph','gasoline',\
                       'gift','grade','goose','gravity','Greece','guard','gulf','garage','grabbed','grandmother'],
                  'h':['had','has','have','he','help','her','here','him','his','home','house','how','half','hand',\
                       'hard','heard','high','himself','however','happened','having','heart','heavy','held','hold',\
                       'horse','hot','hour','hundred','hair','happy','''he's''','heat','history','human','happen',\
                       'Henry','higher','hit','hole','hope','huge','hardly','hat','hill','hurt','herself','hungry',\
                       'handle','height','hung','hurry','hall','''he'd''','health','highest','hunt','''hadn't''',\
                       'harder','hide','hurried','''haven't''','helpful','hidden','honor','husband','hearing',\
                       'highway','halfway','hang','''he'll''','headed','herd','hollow','handsome','harbor','hay',\
                       'hello','horn','hospital','habit','happily','Harry','heading','hunter'],
                  'i':['I','if','in','into','is','it','its','''I'll''','''I'm''','idea','important','inside','ice',\
                       'Indian','instead','itself','''I've''','inch','information','iron','interest','island',\
                       '''isn't''','''I'd''','imagine','include','indeed','instrument','immediately','industry',\
                       'instance','Italy','including','increase','indicate','individual','identity','importance',\
                       'impossible','India','invented','Italian','involved','improve','influence','income',\
                       'industrial','introduced','ill','interior','Illinois','image','independent','instant'],
                  'j':['just','John','job','Jim','Joe','Jack','Johnny','joined','Jane','join','jump','James','Japanese',\
                       'jar','journey','joy','Japan','jet','Jimmy','July','June','Johnson','Jones','judge','Jeff',\
                       'jungle','January'],
                  'k':['know','kept','King','key','kitchen','knowledge','knife','kill','kids'],
                  'l':['large','last','left','like','line','little','long','look','land','later','learn','let',\
                       'letter','life','light','live','living','language','lay','least','leave','''let's''','list',\
                       'longer','low','larger','late','leg','length','listen','lost','lot','lower','lady','largest',\
                       'lead','led','level','love','law','lie','laid','liquid','loud','lake','Latin','leader',\
                       'leaving','likely','lunch','laugh','library','lift','lion','local','lose','lovely','lying',\
                       'lesson','Lincoln','lips','log','London','loose','layers','leaf','leather','load','lonely',\
                       'Louis','lack','lamp','locate','luck','loss','lucky','labor','limited','location','label',\
                       'Lee','lungs'],
                  'm':['made','make','man','many','may','me','men','might','more','most','Mr.','must','my','making',\
                       'mean','means','money','morning','mother','move','Mrs.','main','map','matter','mind','Miss',\
                       'moon','mountain','moving','music','machine','mark','maybe','measure','meet','middle','milk',\
                       'minute','modern','moment','month','mouth','Mary','material','meant','meat','method',\
                       'missing','major','met','metal','movement','market','member','Mexico','Mike','mine','motion',\
                       'myself','mass','master','mile','mix','model','mud','muscle','magic','Mama','manner','Mark',\
                       'May','mostly','massage','minerals','March','meal','medicine','merely','mice','molecular',\
                       'musical','mail','married','mighty','mirror','Mississippi','motor','mouse','machinery','mad',\
                       'magnet','Mars','military','mistake','mood','mainly','managed','mental','mixture','movie',\
                       'manufacturing','Martin','mathematics','melted','memory','mill','mission','monkey','Mount',\
                       'mysterious'],
                  'n':['name','never','new','next','no','not','now','number','near','night','nothing','needed',\
                       'notice','natural','nearly','necessary','New York','north','needs','nor','nose','note',\
                       'nation','nature','nine','none','neck','news','nice','noise','noun','nearby','nearest','nest',\
                       'newspaper','nobody','national','neighbour','native','Negro','noon','needle','nodded','numeral',\
                       'nails','naturally','negative','nearer','nervous','noted','neighborhood','Norway','nuts'],
                  'o':['of','off','old','on','one','only','or','other','our','out','over','own','once','open',\
                       'order','outside','object','ocean','oil','opposite','office','older','onto','original',\
                       'oxygen','observe','ordinary','outer','occur','orange','ought','offer','oldest','operation',\
                       'orbit','organized','outline','obtain','origin','owner','October','officer','Ohio','opinion',\
                       'opportunity','organization','occasionally','official','ourselves'],
                  'p':['part','people','place','put','page','paper','parts','perhaps','picture','play','point','past',\
                       'pattern','person','piece','plant','poor','possible','power','probably','problem','pay','per',\
                       'plan','plane','present','product','pair','party','pass','period','please','position','pound',\
                       'practice','pretty','produce','pull','paragraph','parent','particular','path','Paul','Peter',\
                       'pick','president','pressure','process','public','paid','phrase','plain','poem','population',\
                       'proper','proud','provide','purpose','putting','Pacific','peace','plate','plenty','popular',\
                       'powerful','push','parallel','park','particularly','pencil','perfect','planet','planned',\
                       'pleasant','pocket','police','political','post','potatoes','price','printed','program','property',\
                       'prove','paint','Papa','Paris','particles','personal','physical','pie','pipe','pole','pond',\
                       'progress','pack','partly','pet','pine','pink','pitch','pool','prepare','press','prevent',\
                       'pure','pain','pan','pen','piano','pictured','pig','pile','planning','pony','principal',\
                       'production','passage','percent','perfectly','pilot','pleasure','plural','plus','poet','porch',\
                       'pot','powder','previous','primitive','principle','prize','purple','package','pale','plastic',\
                       'Pole','port','pour','private','properly','protection','pupil','palace','Pennsylvania',\
                       'Philadelphia','plates','poetry','policeman','positive','possibly','practical','pride','promised'],
                  'q':['question','quickly','quite','quiet','quick','quietly','quarter','queen'],
                  'r':['read','right','ready','red','remember','rest','room','run','rain','ran','real','river','road',\
                       'rock','round','rather','reach','reason','record','running','race','radio','region','result',\
                       'return','rich','ride','ring','rule','report','rope','rose','row','raise','range','rate',\
                       'regular','related','replied','represent','rise','railroad','rapidly','root','rubber','remain',\
                       'riding','roll','Roman','roof','rough','rays','recent','recognize','replace','rhythm','Richard',\
                       'Robert','rod','ruler','rabbit','ranch','realize','receive','recently','rice','rising','rocket',\
                       'refer','religious','repeat','research','respect','review','route','raw','reader','remove',\
                       'rear','refused','roar','Rome','Russia','Russian','recall','relationship','remarkable','require',\
                       'rhyme','rocky','rubbed','rush'],
                  's':['said','same','saw','say','see','she','should','show','small','so','some','something','sound',\
                       'still','such','school','sea','second','seen','sentence','several','short','shown','since',\
                       'six','slide','sometime','soon','space','States','story','sun','sure','sat','scientist','shall',\
                       'ship','simple','size','sky','slowly','snow','someone','special','stand','start','state',\
                       'stay','stood','stop','stopped','strong','suddenly','summer','surface','system','seems','sent',\
                       'seven','shape','sides','single','skin','sleep','smaller','soft','soil','south','speak',\
                       'speed','spring','square','star','step','store','straight','strange','street','subject','suppose',\
                       'sand','science','section','seed','send','sense','sets','sharp','sight','sign','silver',\
                       'similar','sit','son','song','spent','spread','stick','stone','safe','salt','Sam','scale',\
                       'sell','separate','sheep','shoe','shore','simply','sing','sister','sitting','sold','soldier',\
                       'solve','speech','spend','steel','string','student','studied','sugar','scientific','season',\
                       'seat','share','shot','shoulder','slow','smile','solid','solution','sort','southern','stage',\
                       'statement','station','steam','stream','strength','supply','surprise','symbol','sad','sail',\
                       'save','score','seeing','serious','service','sheet','shop','silent','smell','smoke','smooth',\
                       'source','spell','storm','structure','supper','support','sweet','swim','scene','search','secret',\
                       'series','serve','settlers','shinning','shut','signal','Sir','skill','smallest','social',\
                       'softly','St.','struck','studying','success','suit','sunlight','swimming','safety','Sally',\
                       'sang','setting','shells','sick','situation','slightly','Spain','spirit','steady','stepped',\
                       'strike','successful','sudden','sum','Saturday','saved','shade','shadow','shirt','shoot',\
                       'shorter','silence','slipped','Smith','snake','somewhere','spoken','standard','straw','strip',\
                       'substance','suggest','Sunday','silk','slept','spite','stretch','stronger','stuck','swing',\
                       'salmon','screen','seldom','select','society','somebody','specific','spider','sport','stairs',\
                       'stared','steep','stomach','stove','stranger','struggle','surrounded','swam','syllable','saddle',\
                       'settle','shelf','shelter','shine','sink','slabs','slave','somehow','split','stems','stock',\
                       'swept','sale','satellites','satisfied','scared','selection','shake','shaking','shallow','shout',\
                       'silly','simplest','slight','slip','slope','soap','solar','species','spin','stiff','swung'],
                  't':['take','tell','than','that','the','them','then','there','these','they','thing','think','this',\
                       'those','thought','three','through','time','to','together','too','two','table','though','today',\
                       'told','took','top','toward','tree','try','turn','taken','talk','tall','ten','''that's''',\
                       'themselves','third','tiny','town','tried','teacher','thousand','thus','Tom','travel','trip',\
                       'trouble','tail','team','teeth','temperature','test','''there's''','therefore','thick','thin',\
                       'train','television','term','throughout','tired','total','touch','trade','truck','twice',\
                       'type','till','tomorrow','tube','twelve','twenty','telephone','Texas','threw','throw','tone',\
                       'tool','track','trail','taste','taught','thank','''they're''','tip','title','tongue','terrible',\
                       'tie','traffic','teach','tears','thirty','Thomas','thread','throat','tight','tin','triangle',\
                       'truth','task','tax','tea','tent','thee','theory','thrown','tonight','topic','tower',\
                       'transportation','trick','tank','tape','thou','tightly','Tim','trace','tribe','trunk','TV',\
                       'thy','tide','torn','troops','tropical','typical','tales','thumb','tobacco','toy','trap',\
                       'treated','tune'],
                  'u':['under','up','us','use','United','until','upon','using','usually','unit','uncle','unless',\
                       'useful','usual','understanding','upper','unusual','union','underline','unknown','upward',\
                       'universe','unhappy','University'],
                  'v':['very','voice','village','various','value','verb','visit','valley','variety','vowel','view',\
                       'valuable','vast','vegetable','volume','Virginia','visitor','vote','vertical','victory',\
                       'voyage','vapor','vessels'],
                  'w':['want','water','way','we','well','went','were','what','when','where','which','while','who',\
                       'why','will','with','word','work','world','would','write','was','white','whole','wind',\
                       'without','walk','warm','watch','weather','whether','wide','wild','winter','within','writing',\
                       'written','wall','war','''wasn't''','week','whose','window','wish','women','''won't''','wood',\
                       'wrote','wait','Washington','wave','''we'll''','weight','west','wife','''wouldn't''','wrong',\
                       'wear','''what's''','wheel','William','wing','wire','won','wonder','worker','''we're''',\
                       'wet','wooden','worth','wagon','western','whatever','wheat','whenever','whom','win','wonderful',\
                       'wore','wash','weak','whale','wise','warn','whispered','wool','waste','''we've''','wherever',\
                       'willing','worry','worse','weigh','Wilson','welcome','''weren't''','whistle','widely','worried',\
                       'wrapped','writer','wealth','wolf'],
                  'x':[],
                  'y':['year','you','your','yes','yet','young','yellow','''you're''','yourself','''you'll''','yard',\
                       '''you've''','yesterday','''you'd''','youth','younger'],
                  'z':['zero','zoo']
                  }
    #Program to find the common words
    if len(word) == 1:
        word = word.lower()
        List = Dictionary[word[0]]
        options = List[0:8]
        return options
    elif len(word) == 2:
        word = word.lower()
        List = Dictionary[word[0]]
        options = []
        for item in List:
            if word == item[0:len(word)]: options.append(item)
        return options
    else:
        word = word.lower()
        if options == [] and len(word) != 0:
            List =  Dictionary[word[0]]
        else:
            List = options
        options = []
        for item in List:
            if word == item[0:len(word)]: options.append(item)
        return options
