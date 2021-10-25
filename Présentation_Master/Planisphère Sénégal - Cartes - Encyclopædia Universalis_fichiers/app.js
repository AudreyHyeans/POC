/****************************************/
/*             RESSOURCES               */
/****************************************/
/*
	player		=>	https://0.s3.envato.com/files/104698258/index.html
	onScroll	=>	https://css-tricks.com/reading-position-indicator/
				=>	http://webdesign.tutsplus.com/tutorials/how-to-build-a-page-scroll-progress-indicator-with-jquery-and-svg--cms-20881
	Masonry		=>	http://masonry.desandro.com/
	Google Font Loader => https://github.com/typekit/webfontloader
*/
//----------------------------------------


(function(document,navigator,standalone) {
    if ((standalone in navigator) && navigator[standalone]) {
        var curnode, location=document.location, stop=/^(a|html)$/i;
        document.addEventListener('click', function(e) {
            curnode=e.target;
            while (!(stop).test(curnode.nodeName)) {
                curnode=curnode.parentNode;
            }
            if('href' in curnode && ( curnode.href.indexOf('http') || ~curnode.href.indexOf(location.host) ) ) {
                e.preventDefault();
                location.href = curnode.href;
            }
        },false);
    }
})(document,window.navigator,'standalone');

/* if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').then(function(registration) {
      // Registration was successful
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      // registration failed :(
      console.log('ServiceWorker registration failed: ', err);
    });
  });
} */

		var gap = 54;
$(function() {
	// patch recherche pour virer les param et avoir la bonne URL
	if(pageIsOn('recherche')){
		paramURL = getUrlVars();
		if(paramURL['q']){
			if(paramURL['classif'])
				window.location.href = "/recherche/q/"+paramURL['q']+"?r=1&classif="+paramURL['classif'];
			else
				window.location.href = "/recherche/q/"+paramURL['q'];
		}
	}
	// go to
	url = window.location.href;
	// if niveau
	if(url.indexOf("#c") > -1 || url.indexOf("#i") > -1){
		anchor = "#"+url.split("#").pop();
		$(".sommaire li").removeClass('active');
		$(".sommaire a[href="+anchor+"]").closest('li').addClass('active');

		// si on pointe sur un chaptire
		if(url.indexOf("#c") > -1){
			target = anchor;

		}
		// si on pointe directement sur l'index
		if(url.indexOf("#i") > -1)
			target = "#"+$(anchor).parent().parent().prev(".chapter-title").prop('id');

		findInSommaire(anchor);
		/* tar = $(target).offset().top-$("#nav-desktop").height()-50;
		$('html,body').animate({scrollTop:tar}, 500, function(e){
			$("#callColonne").fadeIn();
			$("#callColonne").trigger('click');
		}); */
		tar = $(href).offset().top-65-gap-ctaHeight-nlHeight;
		absPosition = tar;
		window.scrollTo(0, tar);
		setTimeout(function(){ $("#callColonne").trigger('click'); }, 300);
	}
	// EOF go to

	// Pour citer
	if($(".eu-date").length > 0){
		myDate = new Date();
		month = new Array('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre');
		currentDate = myDate.getDate() +" "+ month[myDate.getMonth()] +" "+ myDate.getFullYear();
		$(".eu-date").html(currentDate);
	}
	// EOF

	$(document).on('click','a[href^="#"], .anchor', function(event){
    	event.preventDefault();
    	href = this.hash;
    	if(href != "" && $(this).hasClass("anchor")){
			if(href == "#top")
				tar = 0;
			else if($("#nav-mobile").is(':visible'))
				tar = $(href).offset().top-$("#nav-mobile").height()-10;
			else
				tar = $(href).offset().top-$("#nav-desktop").height()-50;

			window.scrollTo(0, tar-gap);
//			$('html,body').animate({scrollTop:tar}, 500);
		}
	});


$(".menu-btn").on('click',function(e){
	e.preventDefault();
	$("body").addClass('open-left');
	$(".drawer *[data-action=close]").trigger('click');
});
$('.site-overlay').on('click',function(e){
	e.preventDefault();
	$("body").removeClass('open-left');
});
/*********************************/
/*           ARTICLE             */
/*********************************/
	if($("#corps-fr").length > 0){
		/* progress indicator */
		var getMax = function(){
			// $(window).height()
			return $("#corps-fr").height()/* - $(window).height() */;
		}

		var getValue = function(){
	    	return $(window).scrollTop();
		}

		if ('max' in document.createElement('progress')) {
		    // Browser supports progress element
			var progressBar = $('progress');

			// Set the Max attr for the first time
			progressBar.attr({ max: getMax() });

			$(document).on('scroll', function(){
				// On scroll only Value attr needs to be calculated
				progressBar.attr({ value: getValue() });

			});

			/* $(window).resize(function(){
				// On resize, both Max/Value attr needs to be calculated
				progressBar.attr({ max: getMax(), value: getValue() });
				//clearSomm();
			}); */

			$(window).resize(function (){
				progressBar.attr({ max: getMax(), value: getValue() });
			});


		}else{
			var progressBar = $('.progress-bar'), max = getMax(), value, width;

			var getWidth = function() {
				// Calculate width in percentage
				value = getValue();
				width = (value/max) * 100;
				width = width + '%';
				return width;
			}
			var setWidth = function(){
				progressBar.css({ width: getWidth() });
				somm(getWidth());
			}

			$(document).on('scroll', setWidth);
			/*
			$(window).on('resize', function(){
				max = getMax();
				setWidth();
			}); */

			$(window).on('resize',function (){
				max = getMax();
				setWidth();
			});

		}
		//$('#sujet .showmore button').click(function(){$('#sujet .more_sujet').show() ;$('#sujet .showmore').hide() ;return false;});
		$('.display-more').click(function(){$(this).parent().find('.more_sujet').show() ;$(this).hide() ;return false;});

		// pour afficher les <sup> dans les factbox qui ne sont pas des notes
		$(".factbox .value-note sup").each(function(index,value){
			val = $(".factbox .value-note sup").eq(index).text().trim();
			if(isNaN(val))
				$(".factbox .value-note sup").eq(index).show();
		});
	}


/*********************************/
/*          RECHERCHE            */
/*********************************/
	$("body").on('click',function(e){
		if(!pageIsOn('atlas') && $(e.target).closest('#s-desktop').length == 0 && $(e.target).closest('#s-mobile').length == 0){
			$("#search-desktop, #search-mobile").parent().removeClass('has-error');
		}
	});
	$("#search-desktop, #search-mobile").on('keypress',function(e){
		$("#search-desktop").parent().removeClass('has-error');
	});

	// Auteurs
	$("*[data-action='searchAuthor']:not(.disabled)").on('click',function(e){
		term = $("#search-desktop").val();
		if($.trim(term).length !== 0)
			window.location = "/recherche/t/auteur/q/"+term;
		else
			$("#search-desktop").parent().addClass('has-error');

	});
	// EOF Auteurs

	// Launch search
	$("form[action*=recherche]").on('submit',function(e){
		e.preventDefault();
		if ($(this).attr("id") != 'searchFormAvancer') {
			val = $(this).find('input[name=q]').val();
			if($.trim(val).length === 0){
				$("#search-desktop, #search-mobile").parent().addClass('has-error');
				$("#search-desktop, #search-mobile").popover('show');
				return false;
			}else{
				window.location.href = "/recherche/q/"+val+"/";
			}
		} else {
			val = $(this).find('textarea[name=q]').val();
			classif = $(this).find('select[name=classif]').val();
			if(classif>0)
				window.location.href = "/recherche/q/"+encodeURIComponent(val)+"/?r=1&classif="+classif;
			else
				window.location.href = "/recherche/q/"+encodeURIComponent(val)+"/?r=1";

		}
	});
	// EOF Launch search

    $("*[data-action='searchTab']").on('click',function(e){
	    setCookie('tabSearch',$(this).data('value'));
    })
    $("*[data-action='switchDisplay']").on('click',function(e){
	    $(this).parent().find('.btn').removeClass('active');
	    $(this).addClass('active');
	    setCookie('switchDisplay',$(this).data('value'));
    });

	if($("#authentification").length > 0){
		if(window.location.hash !=""){
			$("a[href="+window.location.hash+"]").addClass('btn-universalis').trigger('click');
		}
		$("*[data-toggle='tab']").on('click',function(e){
			$('.step').removeClass('btn-universalis').removeClass('active');
			$(this).addClass('active btn-universalis');
			$(this).parent().find('.btn').blur();
		})
	}
/*********************************/
/*        CLASSIFICATION         */
/*********************************/
	if(pageIsOn('classification')){
		$(".breadcrumb").affix({
			offset: {
				top: $("header.header").height()-$("#nav-desktop").height()
			}
		});
	}

/*
	cssDark = [];
	if(isEDU){
		cssDark.push(
		{
			url : "/fileadmin/templates/2017/css/darkmode.edu.css",
			media: "screen",
			id: "css-darkmode-edu"
		})
	}
	if(isFR){
		cssDark.push(
		{
			url : "/fileadmin/templates/2017/css/darkmode.fr.css",
			media: "screen",
			id: "css-darkmode-edu"
		})
	}
	cssDark.push({
			url : "/fileadmin/templates/2017/css/darkmode.css",
			media: "screen",
			id: "css-darkmode"
		});
	if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
		addCSS(cssDark);
	}

	window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
		if(e.matches && $("#css-darkmode").length == 0){
			addCSS(cssDark);
		}
	});
	*/
});