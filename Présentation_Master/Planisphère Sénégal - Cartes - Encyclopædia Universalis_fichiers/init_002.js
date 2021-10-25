var bLazy, isMobile = isDesktop = isTablet = isProspect = isConnected = isFree = isFirefox = isMac = isPC = isEDU = isFR = isPiwik = isAnalytics = popError = false;
var adStatus = "column";
var month = new Array("janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre");
var clicked = searchTerm = "";
var debugColor = isDebug = false;
if(typeof sommaireVisible === "undefined")
	sommaireVisible = false;

var colors = {
	'edu':{
		'normal': '#0798aa',
		'hover': '#066e7b',
		'clair': '#68afbe'
	},
	'fr':{
		'normal': '#536d77',
		'hover': '#3e5158',
		'clair': '#678089'
	}
};

if($("link[rel=icon]").attr('href').indexOf('fav-fr') > -1)
	isFR = true;
else
	isEDU = true;

isDev = location.hostname.indexOf('dev.') > -1;
isPreprod = location.hostname.indexOf('preprod.') > -1 || location.hostname.indexOf('guth') > -1;;

isAnalytics = location.hostname.indexOf('universalis.fr') > -1;
isPiwik = location.hostname.indexOf('universalis-edu.com') > -1;
isPiwikFR = getCookie('piwikfr');

isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
isMac = navigator.userAgent.toLowerCase().indexOf('mac os x') > -1;

if(isDev){
	$("title").prepend('[DEV] ');
}
if(isPreprod){
	$("title").prepend('[PREPROD] ');
}

if(isFR){
	$("html").addClass('site-fr');
}
if(isEDU){
	$("html").addClass('site-edu');
}

if(typeof historique === "undefined")
	historique = "";

pro.ressourceCatalogueId=1;
pro.kiosqueId='UNIVERSALIS';

var ttsPlayer = document.createElement('audio');

var sessionCount = 0, audio = '', video = '', mediaOpened = '';
var speed = 500, over = '', target = '', video = '', timeDrag = false, fontSize = "16px", el;

function gup( name, url ) {
    if (!url) url = location.href;
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( url );
    return results == null ? null : results[1];
}

function getActiveTab(){
	windowWidth = $(document).width();
	if(windowWidth > 991){
		$(".tab-pane").addClass('active');
	}else{
		$(".tab-pane").removeClass('active');
		$($('.nav-pills .active a').attr('href')).addClass('active');
	}
}

// debug pronote
var pronote = false;
if(isEDU > -1)
	var pronote = getCookie('pronoteprof');
if(isEDU > -1 && location.hostname.indexOf("dev.") > -1 && isDebug)
	var pronote = '1';

function initCounter(){
	/* compteurs stats */
	var $article = $('#corps-fr');

	if(typeof nbPages !== "undefined"){
		nbPagesTxt = ' page imprimée';
		if(nbPages > 1)
			nbPagesTxt = "pages imprimées";

		nbPagesTxt = '<strong>'+ nbPages +'</strong> '+ nbPagesTxt;
		$('#countPages').html(nbPagesTxt);
	}
	if(isProspect)
		nbMedias = $article.find('.bandeau-media').length;
	else
		nbMedias = $article.find('.media[data-toggle=media]').length;
	if(nbMedias > 0){
		nbMediasTxt = ' &bull; <strong>'+ nbMedias +'</strong> média';
		if(nbMedias > 1)
			nbMediasTxt += "s";
		$('#countMedia').html(nbMediasTxt);
	}else{
		$('#countMedia').remove();
	}
	/* EOF compteurs stats */
}

$(function() {
	if (isMac) {
		$("html").addClass("mac");
	} else {
		$("html").addClass("other");
	}

	var isDesktop = $("html").hasClass('desktop');
	var isMobile = $("html").hasClass('mobile');
	var isTablet = $("html").hasClass('tablet');

	var isProspect = ($('article').data('mode') == 'p') ? true : false;
	var isFree = ($('article').data('mode') == 'f') ? true : false;

	if($('article').data('mode') == 'c' ||  $("#presentation").text().indexOf('Se connecter') < 0){
		isConnected = true;
	}

	if(("standalone" in window.navigator) && window.navigator.standalone){
		$("html").addClass('webapp');
	}

	if(pageIsOn('classification'))
		$(".navbar-nav").find("a[href='/classification/']").closest('li').addClass('active');
	// EOF

	$("#nav-desktop").prepend('<a href="/" class="pull-left" id="backHome" title="Retour à l\'accueil"></a>');
	if(pronote == '1' && typeof pro !== "undefined"){
		$(".pronote").show();
		pro.url += "?sso_id=10415";
		pronoteActivated("#pronote",pro);
	}

	// lazyload images natif vs. lazyload images vieux navigateurs
	if ('loading' in HTMLImageElement.prototype) {
		$(".b-lazy").each(function(e,i){
			$(this).attr('loading','lazy').attr('src',$(this).data('src')).removeClass('b-lazy');
		});
	} else {
		$("body").append('<script type="text/javascript" src="/fileadmin/templates/2017/js/lib/blazy.min.js"></script>');
		bLazy = new Blazy({
			selector: '.b-lazy'
		});
		$('button[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			if(typeof bLazy !== "undefined")
				bLazy.revalidate();
		});
	}

	if(typeof historique !=='undefined' && typeof saveURL == 'function')
		saveURL(historique);

	$("a[href=#]").on('click',function(e){
		e.preventDefault();
		$(this).blur();
	});
	$('button, a, .btn').on('click',function(){
		$(this).blur();
	});
	$("*[rel=external]").on('click',function(e){
		e.preventDefault();
		window.open($(this).attr("href"));
		return false;
	});

	$("#s-mobile input").on('focus',function(e){
		e.preventDefault();
	})
	$("*[data-action=focusSearch]").on('click',function(e){
		e.preventDefault();
		$("input[name=q]:visible").focus();
	})

	$("*[data-toggle=window]").on('click',function(e){
		url = $(this).data('target');
		if(e.target.className.indexOf('fa') == -1 )
			window.location.href = url;
	});
});
(function() {
    var ev = new $.Event('classadded'),
        orig = $.fn.addClass;
    $.fn.addClass = function() {
        $(this).trigger(ev, arguments);
        return orig.apply(this, arguments);
    }
})();