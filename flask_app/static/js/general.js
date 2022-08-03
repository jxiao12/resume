window.onload=function(){
    var oDiv=document.getElementById('div1');
    var oUl=oDiv.getElementsByTagName('ul')[0];
    var aLi=oUl.getElementsByTagName('li');
    var leftbutton=document.getElementById('left button');
    var rightbutton=document.getElementById('right button');
    var timer=null;
    var iSpeed=5;
    oUl.innerHTML+=oUl.innerHTML;
    oUl.style.width=aLi.length*aLi[0].offsetWidth+'px';
    function fnMove(){
        if(oUl.offsetLeft<-oUl.offsetWidth/2){
            oUl.style.left=0;
        }else if(oUl.offsetLeft>0){
            oUl.style.left=-oUl.offsetWidth/2+'px';
        }
        oUl.style.left=oUl.offsetLeft+iSpeed+'px';

    }
    timer=setInterval(fnMove,60);
    leftbutton.onclick=function(){
        iSpeed=-5;

    }
    rightbutton.onclick=function(){
        iSpeed=5;

    }
    oDiv.onmouseover=function(){
        clearInterval(timer);

    }
    oDiv.onmouseout=function(){
        timer=setInterval(fnMove,30);

    }
};