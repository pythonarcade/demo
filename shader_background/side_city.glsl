#define CityDepth 10
#define Paralax .01
#define CityWidth 1
#define BuildingWidth 10.
//#define BackCol vec4(0.6,0.3,0.05,1)
#define BackCol lerp(vec4(.9,.3,.3,1),vec4(.6,.3,.05,1),.5+.5*sin(iTime))
#define FrontCol vec4(.3,0,.3,1)
#define BalcCol vec4(.2,.1,.3,1)

/*Remove for Low Quality -> */
#define HighQ
/**/

vec4 lerp(vec4 v1,vec4 v2,float t){
    return(v2-v1)*t+v1;
}

float random(vec2 st){
    return fract(sin(dot(st, vec2(12.9898,78.233)))* 43758.5453123);
}
        
float noise(vec2 st){
	vec2 st0=floor(st);
	vec2 st1=.5-cos((st-st0)*3.14)*.5;
	float a0=random(vec2(int(st0.x),int(st0.y)));
	float a1=random(vec2(int(st0.x)+1,int(st0.y)));

	float a2=random(vec2(int(st0.x),int(st0.y)+1));
	float a3=random(vec2(int(st0.x)+1,int(st0.y)+1));

	float b0=(a1-a0)*st1.x+a0;

	float b1=(a3-a2)*st1.x+a2;
	return(b1-b0)*st1.y+b0;
}
        
bool isBuilding(vec2 uv){
	for(int j=-CityWidth;j<=CityWidth;j++){
		for(int n=0;n<5;n++){
			float h=float(n)*.01+(random(vec2(floor(uv.x*BuildingWidth+float(j)),n))-.5)/2.+.25;
			if(h>=uv.y&&
				fract(uv.x*BuildingWidth)-.5-float(j)*1.5<float(CityWidth+1)*1.-float(n)/7.+fract(floor((h-uv.y)*100.*random(vec2(floor(uv.x*BuildingWidth))))/2.)*.1&&
				fract(uv.x*BuildingWidth)-.5-float(j)*1.5>-float(CityWidth-2)*float(n)/7.-fract(floor((h-uv.y)*100.*random(vec2(floor(uv.x*BuildingWidth))))/2.)*.1){
					return true;
			}
		}
	}
	return false;
}

void mainImage(out vec4 fragColor,in vec2 fragCoord)
{
	fragColor = vec4(0);
	vec2 uv=fragCoord/iResolution.xy;
	vec2 sv=uv;
	uv+=noise(uv*10.+iTime)*.002;
	uv.x+=iTime/10.-947.2984;

	bool broke=false;
	for(int i=0;i<CityDepth;i++){
		float mult=iTime*Paralax*float(CityDepth-i);
		if(isBuilding(uv+vec2(mult,0))){
			fragColor+=lerp(BackCol,FrontCol,1./float(i+1));
			broke=true;
			break;
		}
		if(broke){
			break;
		}
		else{
			#ifdef HighQ
			vec4 c=lerp(BackCol,FrontCol,1./float(i+1));
			fragColor+=c*2.*max(0.,.7+.3*noise(vec2(uv.x+mult,float(i)*292.293))-sv.y);
			if(fract(uv.x+mult+.2723)<.1){
				fragColor+=vec4(0,0,.1,0)*max(0.,(8.-uv.y*10.));
			}
			#endif
		}
		uv.x*=1.1;
		uv.y-=1./float(CityDepth)/4.;
	}
	if(!broke){
		fragColor+=lerp(vec4(.9,.5,.2,1),vec4(.01,.01,.2,1.),uv.y);
		float f=noise(vec2(iTime*10.,0)+sv*iResolution.xy*.5);
		if(f>.95&&noise(vec2(iTime*10.,0)+sv*50.)>.5)
		fragColor+=(f-.9)/.1;
	}
}
            