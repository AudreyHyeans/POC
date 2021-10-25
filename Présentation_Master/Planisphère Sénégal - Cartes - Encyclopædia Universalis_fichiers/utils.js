var addCSS = function(cssFiles){
	cssFiles.forEach(function(file,i){
		var link = document.createElement('link');
		link.rel = 'stylesheet';
		link.type = 'text/css';
		link.href = file.url;
		link.media = file.media;

		if(file.rel){
			link.rel = file.rel;
			link.as = "stylesheet";
		}
		if(file.id){
			link.id = file.id;
		}else{
			link.id = "css-"+Date.now();
		}
		var addHeader = document.getElementsByTagName('script')[0];
		addHeader.parentNode.insertBefore(link, addHeader);
	})
}

$.fn.removeClassLike = function(name) {
    return this.removeClass(function(index, css) {
        return (css.match(new RegExp('\\b(' + name + '\\S*)\\b', 'g')) || []).join(' ');
    });
};

if(typeof _paq === "undefined"){
	var _paq = _paq || [];
}

var objToday = new Date(),
	dayOfMonth = (objToday.getDate() == 1) ? objToday.getDate() +"er" : objToday.getDate() +"",
	months = new Array('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'),
	curMonth = months[objToday.getMonth()],
	curYear = objToday.getFullYear(),
	today = dayOfMonth +" "+ curMonth +" "+ curYear;

if(location.pathname.indexOf("/media/") < 0){
	Array.prototype.unique = function()
	{
	    var tmp = {}, out = [];
	    for(var i = 0, n = this.length; i < n; ++i)
	    {
	        if(!tmp[this[i]]) { tmp[this[i]] = true; out.push(this[i]); }
	    }
	    return out;
	}


	String.prototype.replaceAll = function(search, replacement) {
	    var target = this;
	    return target.split(search).join(replacement);
	};
}

$.fn.toggleLoading = function(e){
	this.each(function(){
		if($(this).hasClass('disabled')){
			$(this).removeClass('disabled');
			$(this).prop('disabled',false);
			if($(this).find('i').length == 1){
				className = $(this).find('i').data('original');
				$(this).find('i').removeClass('fa fa-circle-o-notch fa-spin').addClass(className);
			}
		}else{
			$(this).addClass('disabled');
			$(this).prop('disabled','disabled');
			if($(this).find('i').length == 1){
				className = $(this).find('i').attr('class');
				$(this).find('i').attr('data-original',className).removeClass(className).addClass('fa fa-circle-o-notch fa-spin');
			}
		}
		return $(this);
	});
}


var debounce = function (func) {
  var timer = void 0;
  return function (event) {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(func, 100, event);
  };
};

function arrayMin(arr) {
  return arr.reduce(function (p, v) {
	 if(p == "")
	 	return v;
	 else if(v == "")
	 	return p;
	 else
	 	return ( p > v ? p : v );
  });
}

function arrayMax(arr) {
  return arr.reduce(function (p, v) {
	  	 if(p == "")
	 	return v;
	 else if(v == "")
	 	return p;
	 else
    return ( p < v ? p : v );
  });
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
    function(m,key,value) {
      vars[key] = value;
    });
    return vars;
  }


function striptags(html){
   var doc = new DOMParser().parseFromString(html, 'text/html');
   return doc.body.textContent || "";
}

function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value+'; path=/';
}

function getCookie(c_name) {
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == c_name) {
            return unescape(y);
        }
    }
	return false
}

function navigation(infos){
	if(typeof infos.title !== "undefined")
		title = infos.title;
	else
		title = null;
	history.pushState(infos, title, infos.url);
	//history.replaceState({nref: infos.nref},null, infos.url);
}

function pushState(value){
	url = window.location.href;
	url_replace = value;
	history.pushState(stateObj,value,url_replace);
	window.history.pushState({},value, url_replace);
}

function isPortrait() {
    return window.innerHeight > window.innerWidth;
}

function visibility(obj) {
	var winw = jQuery(window).width(), winh = jQuery(window).height(),
		elw = obj.width(), elh = obj.height(),
		o = obj[0].getBoundingClientRect(),
		x1 = o.left - winw, x2 = o.left + elw,
		y1 = o.top - winh, y2 = o.top + elh;

	return [
		Math.max(0, Math.min((0 - x1) / (x2 - x1), 1)),
		Math.max(0, Math.min((0 - y1) / (y2 - y1), 1))
	];
}

function noop() {};

function nl2br (str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}

function getViewport(){
	if (document.compatMode === 'BackCompat') {
	    return document.body.clientHeight;
	} else {
	    return document.documentElement.clientHeight;
	}
}

function close(){
	over = '';
	$("body").css('overflow','visible');
	if(video != "")
		video[0].pause();
	if(audio != "")
		audio[0].pause();

	video = "";
	audio = "";
	el = "";

	$(".media-over").fadeOut();
	if(over == 'media'){
		/* $('.media-legend').hide(); */
		$('.action-legend').removeClass('active');
		$('.media-element').lhpMegaImgViewer('destroy');
	}
	$('.media-legend').show();
}



/*********************************/
/*         STATISTIQUES          */
/*********************************/
//temporaire, tous les appels à modifier vers stats()
function statsPiwik(url, title, referer){
	stats(url, title, referer)
}

function stats(url, title, referer){
	if(isPiwik || isPiwikFR){
		if(typeof _paq === "undefined"){
			var _paq = _paq || [];
		}
	 	var u="//"+location.hostname+"/";
	 	if(typeof Piwik !== "undefined"){
		 	var piwikTracker = Piwik.getTracker(u + "ctp.php", 1);

		 	if(!isPiwikFR){
				var piwikRange = 7000000;
				piwikTracker.setDomains('*.universalis-edu.com');
				piwikTracker.setSiteId(piwikRange+parseInt(getCookie('p_eta')));
			}else{
				piwikTracker.setDomains('*.universalis.fr');
				piwikTracker.setSiteId(parseInt(isPiwikFR));
			}
			piwikTracker.setReferrerUrl(referer);
			piwikTracker.setCustomUrl(url);
			piwikTracker.setDocumentTitle(title);
			piwikTracker.trackPageView();
			piwikTracker.enableLinkTracking();
		}
	}
}

function disableScrolling(){
    var x=window.scrollX;
    var y=window.scrollY;
    window.onscroll=function(){window.scrollTo(x, y);};
}

function enableScrolling(){
    window.onscroll=function(){};
}

/**
 * Détermine sur quelle page on est.
 *
 * @param String type : article|document|media|recherche|atlas
 * @returns boolean
 */

function isCurrentPage(page){
	current = window.location.href;
	return (current.indexOf("/"+page+"/") > -1);
}

var pageIsOn = function(typepage){
    //Url en cours
    var win_href =  window.location.pathname;

    if (typepage == 'article' )
    	typepage = 'encyclopedie';

    var pattern = new RegExp('^\/'+typepage+'\/');
    return pattern.test(win_href);

}

function addTrackEvent(eventCategory, eventName, eventValue){
	if(isEDU){
		_paq.push(['trackEvent', eventCategory, eventName, eventValue]);
	}
	else{
		_gaq.push(['_trackEvent', eventCategory, eventName,  eventValue]);
	}
}

 function isFile(url){
	if(url){
		var req = null;

		if (window.XDomainRequest) {
			req = new XDomainRequest();
		} else if (window.XMLHttpRequest) {
			req = new XMLHttpRequest();
		} else {
			return false;
		}
		req.open('HEAD', url, false);
		req.send();
		if(req.status==200 && req.responseURL.indexOf('404.html') < 0)
			return true;
		else
			return false;
	}else{
		return false;
	}
}

function sameStrings(arr1){
	var arr= arr1.concat().sort(),
	a1= arr[0], a2= arr[arr.length-1], L= a1.length, i= 0;
	while(i< L && a1.charAt(i)=== a2.charAt(i)) i++;
	return a1.substring(0, i);
}