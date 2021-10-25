var isGDPRMode = function(){return true}

// pour simuler les fonctions xajax
var xajaxRequestUri="/xajax-ctrl";
var xajaxDebug=false;
var xajaxStatusMessages=true;
var xajaxWaitCursor=false;
var xajaxDefinedGet=0;
var xajaxDefinedPost=1;
var xajaxRewritedGet=2;

if(typeof hightlight_documents === "undefined"){
	var hightlight_documents = function(){
		return false;
	}
}
if(typeof getFavori === "undefined"){
	var getFavori = function(){
		return false;
	}
}
if(typeof fillFieldDialogAddfavori === "undefined"){
	var fillFieldDialogAddfavori = function(){
		return false;
	}
}
if(typeof getIdDico === "undefined"){
	var getIdDico = function(){
		return false;
	}
}
if(typeof tx_eu_getEducArteLink === "undefined"){
	var tx_eu_getEducArteLink = function(){
		return false;
	}
}
if(typeof tx_eu_checkGescom === "undefined"){
	var tx_eu_checkGescom = function(){
		return xajax.call("_checkGescom", arguments, 2);
	}
}

if(typeof saveURL === "undefined"){
	var saveURL = function(){
		return false;
	}
}

// EOF


if(typeof showDicoFr === "undefined"){
	var showDicoFr = function(){
		return false;
	}
}

// gestion du formulaire de connexion, qui n'intéresse que FR && prospect
function verifLogin(field){
	if(field.value != ""){
		surligne(field, false);
		return true;
	}else{
		surligne(field, true);
		return false;
	}
}

function verifPassword(field){
	if(field.value != ""){
		surligne(field, false);
		return true;
	}else{
		surligne(field, true);
		return false;
	}
}

function verifForm(f){
	var l = verifLogin(f.f_login);
	var p = verifPassword(f.f_password);
	return (l && p) ? true : false;
}

function surligne(field, erreur){
	field.style.backgroundColor = (erreur) ? "#fba" : "";
}
// EOF


$(function() {
	// on vire les 2 derniers éléments du menu déroulant recherche
	$("#searchOptions").find('li').slice(-2).remove();

	/** sommaire flottant **/
	$("#floating-somm .menu").css('max-height',window.innerHeight-160);
	$("#floating-somm").addClass('open').show();
	$(document).on('click','[data-action=hideSomm]', function(e){
		$('#floating-somm').removeClass('open');
		$('#floating-somm').find('.menu').hide();
	});
	$(document).on('click','[data-action=toggleSomm]', function(e){
		$('#floating-somm').toggleClass('open');
		$('#floating-somm').find('.menu').toggle();
	});
	$(window).on('resize',function(e){
		$("#floating-somm .menu").css('max-height',window.innerHeight-160);
	});
	/** EOF **/

	/** media **/
	$(".media[data-player]").on('click',function(e){
		id = $(this).data('target').replace('#','');
		window.location.href = '/media/'+id+'/';
	});
	/** EOF **/

	// possiblement à supprimer -_-
	$("*[role='log']").remove();
	$(".qc-cmp-persistent-link").remove();
	// EOF

	$(".fav-media").remove();

	var isDesktop = $("html").hasClass('desktop');
	var isMobile = $("html").hasClass('mobile');
	var isTablet = $("html").hasClass('tablet');

	if(isDesktop){
		$(window).on('resize',function(e){
			/* if($(window).width() < 991 && adStatus == "column"){
				$("#corps-prospect").find('p').first().before($("#navigation"));
				adStatus = "body";
			}
			if($(window).width() >= 991 && adStatus == "body"){
				$("#medias-fr").prepend($("#navigation").removeClass('pull-right'));
				adStatus = "column";
			}
			if($(window).width() < 991){
				if($(window).width() > 500)
					$("#navigation").addClass('pull-right');
				else
					$("#navigation").removeClass('pull-right');
			}else
				$("#navigation").removeClass('pull-right');
				*/
			if($(window).width() < 991){
				$(".menu").hide();
			}else{
				$(".menu").show();
			}
		})
	}

	// pour gérer le bouton / menu / pub
	if(isTablet){
		$('#floating-somm').css('bottom',$("#a-bandeau").height()+20);
	}

	$(document).on("click","#callSommaire",function(e){
		$(".menu").show();
	});

	$("*[data-action=closeSomm]").on('click',function(e){
		$(".menu").hide();
	});
	if($("#callSommaire").length == 0 && !pageIsOn('media')  && window.location.pathname != "/" && !pageIsOn('accueil')){
		$("body").append('<button id="callSommaire" data-target="fr" class="visible-xs btn btn-sm btn-universalis hidden-print" style="bottom: 100px"><i aria-hidden="true" class="fa fa-chevron-up"></i> Sommaire</button>');
	}
	// EOF


	var cssFiles = [
	{
		'url': '/fileadmin/templates/2017/css/lib/bootstrap/min/bootstrap.print.min.css',
		'media': 'print'
	},{
		'url': '/fileadmin/templates/2017/css/print.css',
		'media': 'print'
	}];

	addCSS(cssFiles);

	tx_eu_checkGescom();
});
