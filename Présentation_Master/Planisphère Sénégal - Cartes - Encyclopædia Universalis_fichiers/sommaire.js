var ctaHeight = nlHeight = citationPosition = navigationHeight = ctaHeight = movableHeight = ctaJuniorHeight = nativeHeight = totalHeight = 0;
var absPosition = startPosition = scrollPosition = "";
var breakPoint = 767;
var lastScrollTop = 0;
var calledClick = false;
var initPos = "";
var gap = 54;
function findPos(id) {
	var node = document.getElementById(id);
	var curtop = 0;
	var curtopscroll = 0;
	if (node.offsetParent) {
		do {
			curtop += node.offsetTop;
			curtopscroll += node.offsetParent ? node.offsetParent.scrollTop : 0;
		} while (node = node.offsetParent);

		return(curtop - curtopscroll);
	}
}

function findInSommaire(anchor){
	flag = false;
	// niveau 1
	if($(".sommaire a[href=#"+anchor+"]").next('ul').length > 0 && $(".sommaire a[href=#"+anchor+"]").closest('li').hasClass('somm-h2')){
		$(".sommaire a[href=#"+anchor+"]").next('ul').slideDown();
		flag = true;
	}

	// niveau 2
	if($(".sommaire a[href=#"+anchor+"]").parent().parent() && $(".sommaire a[href=#"+anchor+"]").closest('li').hasClass('somm-h3')){
		$(".sommaire a[href=#"+anchor+"]").parent().parent().slideDown();
		flag = true;
	}

	// niveau 3
	if($(".sommaire a[href=#"+anchor+"]").parent().parent().parent().parent() && $(".sommaire a[href=#"+anchor+"]").closest('li').hasClass('somm-h4')){
		$(".sommaire a[href=#"+anchor+"]").parent().parent().parent().parent().slideDown();
		flag = true;
	}

	// niveau 4
	if($(".sommaire a[href=#"+anchor+"]").parent().parent().parent().parent().parent().parent() && $(".sommaire a[href=#"+anchor+"]").closest('li').hasClass('somm-h5')){
		$(".sommaire a[href=#"+anchor+"]").parent().parent().parent().parent().parent().parent().slideDown();
		flag = true;

	}
	if(flag)
		$(".sommaire a[href=#"+anchor+"]").closest('.somm-h2').find('i').removeClass('fa-chevron-circle-right').addClass('fa-chevron-circle-down');
}

function scrollSpyIn(id){
	if($(".sommaire li").is('[data-target]'))
		selector = "data-target";
	else
		selector = "href";
	$(".somm-h2 > ul").not($("a["+selector+"=#"+id+"]").closest('.somm-h2').find('ul')).hide();
	$(".sommaire li a.hasChildren i").removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-right');
	findInSommaire(id);
	$(".sommaire li").removeClass('active');
	$("a["+selector+"=#"+id+"]").closest('li').addClass('active');
}


if($("#somm-lycee").length > 0)
	startPosition = $("#somm-lycee").offset().top;

function somm(position){
	scrollPosition = position;
	if($("#callColonne").length > 0 && $(window).width() > 990){
		var sommPosition = $("#somm-lycee .nav-stacked").offset().top;
		if(position > $("#corps-fr").offset().top){
			$("#callColonne").fadeIn();
			absPosition = scrollPosition-$("#somm-lycee .nav-stacked").innerHeight()-$("#nav-desktop").innerHeight()-$("#aff").height()+startPosition;
		}else{
			$("#callColonne").hide();
			$("#somm-lycee").css({'margin-top':0})
		}
	}
}

function clearSomm(){
	if($(window).width() > 990){
		$("#somm-lycee").css({'margin-top':absPosition})
	}else{
		$("#somm-lycee").css({'margin-top':'-300%'})
	}
}

$(function() {
	if($("#callSommaire").length == 0){
		if(isConnected)
			$("body").append('<button id="callSommaire" data-target="fr" class="visible-xs btn btn-sm btn-universalis hidden-print"><i aria-hidden="true" class="fa fa-chevron-up"></i> Sommaire</button>');
	}
	if(initPos == ""){
		if($('.movable').length > 0)
			initPos = $('.movable').offset().top;
		else
			initPos = 0;
	}

	if($("#citation").length > 0)
			citationPosition = $("#citation").offset().top;
		else
			citationPosition = totalHeight;

	$("#callColonne").on('click',function(e){
		var totalHeight = $("#corps-fr").height();
		if($("#navigation").length > 0)
			navigationHeight = $("#navigation").height();
		if($("#cta-senior").length > 0)
			ctaHeight = $("#cta-left").height();
		if($("#cta-junior").length > 0)
			ctaJuniorHeight = $("#cta-junior").height();
		if($(".movable").length > 0)
			movableHeight = $(".movable").innerHeight();
		if($(".native").length > 0)
			nativeHeight = $(".native").height();
		if($("#content_block_newsletter").length > 0)
			nlHeight = $("#content_block_newsletter").innerHeight();

		// on vérifie par rapport au dernier bloc citation, histoire de pas descendre le sommaire trop bas
		if(absPosition-initPos-navigationHeight-ctaHeight-ctaJuniorHeight-nlHeight-nativeHeight-60+movableHeight < 0)
			$("#somm-lycee").css({'margin-top':0})
		else if(citationPosition < parseInt(absPosition + movableHeight)){
			$("#somm-lycee").css({'margin-top':totalHeight-movableHeight})
		}
		else{
			$("#somm-lycee").css({'margin-top':absPosition-initPos-nlHeight+60+gap}) //-navigationHeight-ctaHeight-ctaJuniorHeight-nlHeight-margin+movableHeight
		}
	})

	$("#somm-lycee a.anchor").on('click',function(e){
		if($(window).width() > breakPoint){
			e.preventDefault();
			if($("#cta-senior").length > 0)
				ctaHeight = $("#cta-senior").height();
			if($("#content_block_newsletter").length > 0)
				nlHeight = $("#content_block_newsletter").height();

			calledClick = true;
			$(".sommaire li").removeClass('active');
			$(".sommaire li a.hasChildren i").removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-right');
			$(".somm-h2 > ul").not($(this).closest('.somm-h2').find('ul')).hide();

			href = this.hash;
			findInSommaire(href.replace("#",""));
			if(href != "" && $(this).hasClass("anchor")){
				if(href == "#c_1" || href == "#c_top"){
					tar = 0;
					$(".sommaire").removeAttr('style');
				}
				else{
					//tar = $(href).offset().top+65-ctaHeight-nlHeight;
					/*$("body").animate({scrollTop:tar}, 300, function(e){
						$("#callColonne").trigger('click');
					});*/
					tar = $(href).offset().top-65-gap-ctaHeight-nlHeight;
					absPosition = tar;

 					window.scrollTo(0, tar);
 					setTimeout(function(){ $("#callColonne").trigger('click'); }, 300);
				}
			}
			$(this).closest('li').addClass('active');
		}
	});

	$("*[data-action=menu]").on('click',function(e){
		e.preventDefault();
		if($(this).next('ul').is(':visible')){
			$(this).find('i').removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-right');
		}else{
			$(this).find('i').removeClass('fa-chevron-circle-right').addClass('fa-chevron-circle-down');
		}
		$(this).next('ul').slideToggle();
	})
	if(sommaireVisible){
		$(window).on('scroll', function() {
			if(isConnected || isFree){
				st = $(this).scrollTop();
				absPosition = st;

				if(st < lastScrollTop && $(window).scrollTop() < $("#corps-fr").offset().top){
					somm(0);
					$(".sommaire li").removeClass('active');
					$(".sommaire a[href=#c_1]").closest('li').addClass('active');
					$(".sommaire li a.hasChildren i").removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-right');
					$(".somm-h2 > ul").hide();
				}
				if($(window).scrollTop() < $("#corps-fr").offset().top || $(window).scrollTop() > citationPosition){
					$("#callColonne").fadeOut();
					$("#positionInPage").fadeOut();
				}else{
					$("#callColonne").fadeIn();
					$("#positionInPage").fadeIn();
				}
				lastScrollTop = st;
				text = $(".sommaire li.active > a").text();
				$(".positionInText").html("Chapitre : <em>"+text+"</em>");
				// homemade scrollspy
				// titres
				$(":header[id^=c_]").each(function(e){
					id = $(this).prop('id');
					rec = visibility($(this));
					if(rec[1] < 1 && rec[1] > 0.99){
						scrollSpyIn(id);
					}
				})
				// sources
				$(".sources[id^=s_]").each(function(e){
					id = $(this).prop('id');
					rec = visibility($(this));
					if(rec[1] < 1 && rec[1] > 0.94){
						scrollSpyIn(id);
					}
				})
				// EOF
			}
	    });
	}


	$(window).on('resize', function(){
		absPosition = scrollPosition-$("#somm-lycee .nav-stacked").height()-$("#nav-desktop").height();
	});


	$(document).on("click","#callSommaire",function(e){
		console.log('ccc');
		$("#somm-lycee").css('margin-top',0);
		$("body").css('overflow','hidden');
	});

	$("*[data-action=closeSomm]").on('click',function(e){
		e.preventDefault();
		$(".sommaire, body").removeAttr('style');
	})

	$(".sommaire ul a").on('click',function(e){
		$("*[data-action=closeSomm]").trigger('click');
	});

	if(isDesktop){
		$("body").append('<div class="positionInText" style="display: none">Chapitre : <em>Introduction</em></div>');
		$("progress").on('mouseenter',function(e){
			$(".positionInText").show();
		})
		$("progress").on('mouseleave',function(e){
			$(".positionInText").hide();
		})
	}
});