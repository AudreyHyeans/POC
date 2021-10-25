if(typeof forbiddenDisplay === "undefined")
	var forbiddenDisplay = Array('/abonnement/','/','/accueil/','/essai7jours/','/identification/','/identification/motdepasse/');

var isMobile={Android:function(){return navigator.userAgent.match(/Android/i)},BlackBerry:function(){return navigator.userAgent.match(/BlackBerry/i)},iOS:function(){return navigator.userAgent.match(/iPhone|iPad|iPod/i)},Opera:function(){return navigator.userAgent.match(/Opera Mini/i)},Windows:function(){return navigator.userAgent.match(/IEMobile/i)||navigator.userAgent.match(/WPDesktop/i)},any:function(){return isMobile.Android()||isMobile.BlackBerry()||isMobile.iOS()||isMobile.Opera()||isMobile.Windows()}};
var forbiddenDisplay = Array('/abonnement/','/','/accueil/','/essai7jours/','/identification/','/identification/motdepasse/');
// CTA Universalis
var urls = ["encyclopedie", "classification", "dictionnaire", "chronologie", "evenement", "atlas", "auteurs", "dossier-du-mois", "dossier"], tag = "global", device_type = "";
urls.forEach(function(e){
	if(window.location.href.indexOf('/'+e+'/') > -1)
		tag = e;
});
if(isMobile.any() !== null)
	device_type = "Mobile";
else
	device_type = "Desktop";

var checkVisible = function(elm,height) {
	if(elm !== null){
		var rect = elm.getBoundingClientRect(), viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight);
		return !(rect.bottom-height < 0|| rect.top - viewHeight >= 0-height);
	}
}

var toggleBandeau = function(){
	if($("#a-bandeau").length > 0 && (checkVisible(document.getElementById('cta-top-site'),50) || checkVisible(document.getElementById('cta-article'),68)))
		$("#a-bandeau").removeClass('sticky');
	else
		$("#a-bandeau").addClass('sticky');
}
// penser à modifier lib_article.xsl pour déplacer le menu floating_somm aussi pour les gratuits
var toggleStickyAd = function(){
	if(checkVisible(document.getElementById('cta-col'),0) || checkVisible(document.getElementById('ad_rightslot'),0))
		$("#ad_rightslot2").removeAttr('style');
	else
		$("#ad_rightslot2").css({
			'width': Math.ceil($(".ads").width()),
			'position': 'fixed',
			'top': 0
		});
}

var addCTA = function(){
	if($.inArray(location.pathname,forbiddenDisplay) < 0){
		// CTA
		// mobile
		if(isMobile.any() !== null){
			// footer fixed
			if($("#a-bandeau").length == 0){
				$("body").append('<div id="a-bandeau"></div>');
			}
			$("#a-bandeau").html('<a href="/abonnement/" title="Je veux m\'abonner" onclick="_gaq.push([\'_trackEvent\', \'CTA\', \''+tag+'\', \'['+device_type+'] footer fixed\']);"><img src="/fileadmin/templates/2017/img/cta-footer-fixed.png" alt="" width="610" height="110" class="footer-a" /></a>');
		}
		// eof

		// desktop
		if (isMobile.any() === null) {
			// top article gratuit
			$('#cta-main-top').html( '<p class="text-center mt10"><a href="/abonnement/" onclick="_gaq.push([\'_trackEvent\', \'CTA\',\''+tag+'\', \'['+device_type+'] top free article\']);" title="Abonnez-vous à Universalis pour 1 euro"><img src="/fileadmin/templates/2017/img/cta-top-article.png" width="610" height="110" class="img-max" alt="Abonnez-vous à Universalis pour 1 euro" /><a/></p>' );

			// article col
			$('#cta-col').html('<a href="/abonnement/" class="hidden-xs" onclick="_gaq.push([\'_trackEvent\', \'CTA\',\''+tag+'\', \'['+device_type+'] col right\']);" title="Abonnez-vous à Universalis pour 1 euro"><img src="/fileadmin/templates/2017/img/banner-col-right.png" class="img-max" alt="Abonnez-vous à Universalis pour 1 euro" /></a>');
		}
		// eof

		// all devices

		// article folio number
		$("#folio-number").find('a').each(function(i,e){
			e.attributes[1].nodeValue = e.attributes[1].nodeValue.replace('article folio number','['+device_type+'] article folio number');
		});
		// eof
		// article folio text
		$('#folio-text').html('<a href="/abonnement/" onclick="_gaq.push([\'_trackEvent\', \'CTA\', \''+tag+'\', \'['+device_type+'] article folio text\']);">'+$("#folio-text").text() +'</a>');
		// eof
		// article folio image
		$('#cta-article').html('<a href="/abonnement/" onclick="_gaq.push([\'_trackEvent\', \'CTA\', \''+tag+'\', \'['+device_type+'] article folio image\']);" title="Abonnez-vous à Universalis pour 1 euro"><img src="/fileadmin/templates/2017/img/cta-bottom-article.png" width="610" height="110" class="img-max" alt="Abonnez-vous à Universalis pour 1 euro" /><a/>' );
		// eof

		// EOF
	}

	// home
	if((location.pathname == '/' || location.pathname == '/accueil/') && isMobile.any() === null){
		// CTA colonne droite
		$('#cta-senior').html('<a href="/abonnement/" class="hidden-xs" onclick="_gaq.push([\'_trackEvent\', \'CTA\',\''+tag+'\', \'['+device_type+'] col right\']);" title="Abonnez-vous à Universalis pour 1 euro"><img src="/fileadmin/templates/2017/img/banner-col-right.png" class="img-max" alt="Abonnez-vous à Universalis pour 1 euro" /></a>');
		$('#cta-senior').after('<div id="content_block_newsletter"><h3 class="text-center">Rejoignez-nous</h3><p class="text-center">Inscrivez-vous à notre <strong>newsletter</strong> hebdomadaire et recevez en cadeau un ebook au choix !</p><form onsubmit="return validform(this);" name="tt_address_form" method="post" action="/index.php?id=18175" class="form_nl_slide"><div class="input-group"><input type="email" title="Votre adresse email" class="form-control" id="fe_ttaddress_email_input" name="FE[tt_address][email]" placeholder="Votre adresse email" /><span class="input-group-btn"><button type="submit" class="btn btn-default" style="border-top-left-radius: 0; border-bottom-left-radius: 0; margin-left: -1px"><strong>S\'INSCRIRE</strong></button></span><input type="hidden" name="FE[tt_address][module_sys_dmail_html]" value="1" /><input type="hidden" name="FE[tt_address][first_name]" id="fe_ttaddress_firstname_input" /><input type="hidden" name="FE[tt_address][crdate]" /></div></form></div>');
	}
}


toggleBandeau();
addCTA();
document.addEventListener('scroll', function (event) {
	toggleBandeau();
	toggleStickyAd();
}, true);

window.addEventListener('resize', function (event) {
	toggleStickyAd();
}, true);

$(function() {
	$("#floating-somm").hide();
});
