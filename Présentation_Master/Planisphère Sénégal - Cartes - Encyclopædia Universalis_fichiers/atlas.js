/* https://github.com/timmywil/jquery.panzoom */

var mapTitles = ["carte de situation","carte générale","carte administrative","carte physique","carte relief","carte vierge","découpage administratif"];
var mapLetters = ["S","J","A","P","R","V","L"];
var noSituation = ["AT021700","AT022200","AT021600","AT020700","AT021400"];
var dom = ["AT007000","AT007100","AT007200","AT007300","AT007400","AT007500","AT007600","AT007700","AT007800","AT022700"];

var first = true, hasFav = false, panzoom = "", svgMode = "portrait", ratioSVG = 1, ratioScreen = $(window).width() / $(window).height();
var urlSVG = "/medias/atlas/";
var svg = "", sSVG = "", dSVG = "", fSVG = "", fURL = "", france = false;
var cartesDrawer = breadcrumb = cartes = details = detailsTab = linksTab = notes = limitrophes = event = "";
/***/
var heightComponents = ['height', 'paddingTop', 'paddingBottom', 'borderTopWidth', 'borderBottomWidth'],
    widthComponents = ['width', 'paddingLeft', 'paddingRight', 'borderLeftWidth', 'borderRightWidth'];


var isMobile = isTablet = isDesktop = false;

if($('html').hasClass('desktop'))
	isDesktop = true;
if($('html').hasClass('tablet'))
	isTablet = true;
if($('html').hasClass('mobile'))
	isMobile = true;

var panzoomOpts = {
		linearZoom: true,
		minScale: 0.1,
		maxScale: 3,
		increment: 0.1,
		contain: 'automatic',
		$zoomIn: $("#zoom-in"),
		$zoomOut: $("#zoom-out"),
		$zoomRange: $(".zoom-range"),
		$reset: $("#reset")
	};
if(!isDesktop){
	panzoomOpts.minScale = 1;
	panzoomOpts.increment = 0.5;
}


window.addEventListener('popstate', function(e) {
	if(e.state == null || (typeof e.state.nref !== "undefined" && e.state.nref == null)){
		$("[data-action=atlas-close]").trigger('click');
	}else{
		$("body").addClass('no-scroll');
		if(e.state.hash != null && !$("#modal-atlas").is(':visible')){
			$("body").addClass('no-scroll');
			$("#modal-atlas").fadeIn();
		}
		if($("#modal-atlas").is(':visible')){
			if(e.state.url != window.location.pathname){
				loadingMap();
			}
			var carte = e.state.carte;
			url = urlSVG+e.state.nref.toLowerCase()+".svg";
			$("#cartes").attr('data-media',e.state.nref.toLowerCase());
			showCountry(url, carte,e.state.nref.toLowerCase(), false);
		}
	}
});

function findInObject(stack, needle){
	results = [];
	for(var i=0; i<stack.length; i++) {
		for(key in stack[i]) {
			if(stack[i][key].indexOf(needle)!=-1) {
				results.push(stack[i]);
			}
		}
	}
	return results;
}

function objectFindByKey(array, key, value) {
	cpt = 0;
	indexes = new Array();
    for (var i = 0; i < array.length; i++) {
    	word = no_accent(array[i][key].toLowerCase());
    	pos = word.indexOf(no_accent(value.toLowerCase()));
    	if(pos > -1){ // > -1
    		temp = new Array(i,pos);
			indexes[cpt] = temp;
			cpt++;
		}
    }
    return(indexes);
}

function unique(data){
	var tempMap = {};    // keep track of unique objects with key mapping to the object's key&value
	var distinct = [];    // resulting list containing only unique objects
	var obj = null;
	for (var i = 0; i < data.length; i++) {
	    obj = data[i];
	    for (var key in obj) {        // look in the object eg. {'one':1}
	        if (obj.hasOwnProperty(key)) {
	            if (!tempMap.hasOwnProperty(key + obj[key])) {    // not in map
	                tempMap[key + obj[key]] = obj;        // then add it to map
	                distinct.push(obj);    // add it to our list of distinct objects
	            }
	            break;
	        }
	    }
	}
	return(distinct);
}

var loadingMap = function(){
	$("#atlas-loading").show();
	$("#atlas-map").html("");
	first = false;
	svg = sSVG = dSVG = "";
}

var makeBreadCrumb = function(data){
	bread = [];
	i = 0;
	data.continents.continent.forEach(function(e){
		if(typeof e.attributes.current !== "undefined"){
			bread[i] = {
				url: e.continent_url,
				text: e.continent_name,
				nref: e.attributes.id
			}
			i++;
			if(typeof e.sous_continents !== "undefined"){
				e.sous_continents.sous_continent.forEach(function(ee){
					if(typeof ee.attributes.current !== "undefined"){
					bread[i] = {
						url: ee.sous_continent_url,
						text: ee.sous_continent_name,
						nref: ee.attributes.id

					}
					i++;
					ee.countries.country.forEach(function(eee){
						if(typeof eee.attributes.current !== "undefined"){
							bread[i] = {
								url: eee.country_url,
								text: eee.country_name,
								nref: eee.attributes.id
							}
							i++;
							if(typeof eee.provinces !== "undefined"){
								eee.provinces.province.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.province_url,
											text: eeee.province_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
								eee.provinces.territoire.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.territoire_url,
											text: eeee.territoire_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
							}
							if(typeof eee.regions_metropolitaines !== "undefined"){
								eee.regions_metropolitaines.region_metropolitaine.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.region_metropolitaine_url,
											text: eeee.region_metropolitaine_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
								if(typeof eee.regions_metropolitaines.region_outremer != "undefined"){
									eee.regions_metropolitaines.region_outremer.forEach(function(eeee){
										if(typeof eeee.attributes.current !== "undefined"){
											bread[i] = {
												url: eeee.region_outremer_url,
												text: eeee.region_outremer_name,
												nref: eeee.attributes.id
											}
											i++;
										}
									});
								}
							}
						}
					})
				}
				})
			}
			if(typeof e.countries !== "undefined"){
				e.countries.country.forEach(function(eee){
						if(typeof eee.attributes.current !== "undefined"){
							bread[i] = {
								url: eee.country_url,
								text: eee.country_name,
								nref: eee.attributes.id
							}
							i++;
							if(typeof eee.cantons !== "undefined"){
								eee.cantons.canton.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.canton_url,
											text: eeee.canton_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
							}
							if(typeof eee.provinces !== "undefined"){
								eee.provinces.province.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.province_url,
											text: eeee.province_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
								eee.provinces.territoire.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.territoire_url,
											text: eeee.territoire_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
							}
							if(typeof eee.regions_metropolitaines !== "undefined"){
								eee.regions_metropolitaines.region_metropolitaine.forEach(function(eeee){
									if(typeof eeee.attributes.current !== "undefined"){
										bread[i] = {
											url: eeee.region_metropolitaine_url,
											text: eeee.region_metropolitaine_name,
											nref: eeee.attributes.id
										}
										i++;
									}
								});
								if(typeof eee.regions_metropolitaines.region_outremer != "undefined"){
									eee.regions_metropolitaines.region_outremer.forEach(function(eeee){
										if(typeof eeee.attributes.current !== "undefined"){
											bread[i] = {
												url: eeee.region_outremer_url,
												text: eeee.region_outremer_name,
												nref: eeee.attributes.id
											}
											i++;
										}
									});
								}
							}
						}
					})
			}
		}
	});
	$(".list-atlas").find('.active').removeClass('active');
	$(".list-atlas").find('li .nav.nav-pills.nav-stacked').addClass('hidden');
	$(".list-atlas").find('li.somm-h5 .nav.nav-pills.nav-stacked').removeClass('hidden');
	$(".list-atlas").find('i.fa-folder-open').removeClass('fa-folder-open').addClass('fa-folder');

	if(bread.length > 1){
		bread.forEach(function(e){
			if(typeof e.url !== "undefined"){
				$(".list-atlas").find('a[href="'+e.url+'"]').parent('li').addClass('active').end().next('ul').removeClass('hidden');
			}
		});
		$(".list-atlas").find('a[href="/atlas/"]').parent('li').removeClass('active');
		$(".list-atlas").find('.active > a > i').removeClass('fa-folder').addClass('fa-folder-open');
		$(".list-atlas").find('li.somm-h5 > .atlas-header > i').removeClass('fa-folder').addClass('fa-folder-open');
	}else{
		$(".list-atlas").find('a[href="/atlas/"]').parent('li').addClass('active');
	}


	if(bread.length > 0)
		delete(bread[bread.length-1].url);
	return bread;
}

var svgCalculateSize = function (el) {
    var gCS = window.getComputedStyle(el),
        bounds = {
            width: 0,
            height: 0
        };

    heightComponents.forEach(function (css) {
        bounds.height += parseFloat(gCS[css]);
    });
    widthComponents.forEach(function (css) {
        bounds.width += parseFloat(gCS[css]);
    });
    bounds.ratio = bounds.width / bounds.height;
    panzoomOpts.minScale = bounds.ratio;
    return bounds;
};

var getDrap = function(drap){
	dURL = urlSVG+drap.toUpperCase()+".svg";
	$.get(dURL, function(d){
		dSVG = $(d)[0].firstChild;
	}).fail(function() {
			$("#atlas-error-content").html("drapeau introuvable sur le serveur");
			$("#atlas-error").show();
		});
}

var initTemplates = function(){
	$.get('/fileadmin/templates/2017/templates_atlas.html',function(e){
		$("#tt").html(e);
		cartesDrawer = $("#cartes-drawer-template").html();
		breadcrumb = $("#breadcrumb-template").html();
		cartes = $("#cartes-template").html();
		details = $("#details-template").html();
		detailsTab = $("#details-tab-template").html();
		linksTab = $("#links-tab-template").html();
		notes = $("#details-notes-template").html();
		limitrophes = $("#limitrophes-template").html();
		evenement = $("#event-template").html();
		$("#tt").remove();
	});
}

var applyTemplate = function(opts, data){
	opts.forEach(function(e,i){
		var template = Handlebars.compile(e.template);
		$(e.target).html(template(data));
	})
	$("[data-href]").each(function(e){
		href= $(this).data('href');
		$(this).attr('href',href).removeAttr('data-href');
	})
	$("[data-src]").each(function(e){
		src = $(this).data('src');
		$(this).attr('src',src).removeAttr('data-src');
	});
	if(isFR){
		$("#cartes-list").find('[data-carte=R], [data-carte=V]').hide();
		$("#tab-maps").find('[data-value=R], [data-value=V]').hide();
	}
	if(data.breadcrumb.length == 0){
		$(".breadcrumb").html("<li class='active'><strong>Monde</strong></li>");
	}
	if(data.media_in_articles.attributes.nb > 0){
		$("#atlas-tab-links").removeClass('hidden');
	}else{
		$("#atlas-tab-links").addClass('hidden');
	}
	if(typeof data.fullResult !== "undefined"){
		$("#evenement").removeClass('hidden');
	}else{
		$("#evenement").addClass('hidden');
	}
	// changement du nom des cartes
	if(data.current_element.attributes.type == "monde"){
		$('div[data-value="A"], div[data-carte="A"]').find('p').html('carte des sous-ensembles régionaux');
	}
	if(data.current_element.attributes.type == "continent"){
		$('div[data-value="A"], div[data-carte="A"]').find('p').html('carte politique');
	}
	// EOF
	if(data.current_element.attributes.type == "pays"){
		$(".bloc-limitrophe").removeClass('hidden');
	}else{
		$(".bloc-limitrophe").addClass('hidden');
	}
}

var selectMap = function(carte){
	panzoom.panzoom("zoom", svgSize.ratio*0.5,{silent: true}).panzoom("resetPan",false);
	// on change de carte si la présente n'existe pas dans la nouvelle
	if($("#tab-maps").find('*[data-value='+carte+']').length == 0){
		carte = "A";
		at = $("#tab-maps").find('*[data-value='+carte+']').data('carte');
		newURL = window.location.pathname+"#"+at;
		history.replaceState({nref: at.replace(/.$/,"0")},null, newURL);
	}
	// EOF

	$("#tab-maps").find('*[data-value='+carte+']').trigger('click');
	at = $("#tab-maps").find('*[data-value='+carte+']').data('carte');
	$("#atlas-map").find('title').remove();
	if (typeof at !== "undefined" && at.substring(6,8) >= 0) {

		 if ( $('#listdossiersfavoris').length  ) {

        var tab_fav = new Array();
        //Enregistrer les nref des favoris dans un array
        $('.list-unstyled.fichiers li').each( function(el) {

            //Supprimer doublons
            if ( $.inArray( $(this).data('nref'), tab_fav) === -1 ) {
                tab_fav.push($(this).data('nref'));

            }
        });

        //On est sur la page de recherche
        if ( $('.star_favori').length > 0 ) {
            //Parcourir et chercher si presents dans favoris
            $('.star_favori').each( function(el) {
                if (tab_fav.length>0 &&  $.inArray( $(this).data('nref'), tab_fav) >= 0 ) {
                    $(this).find('.fa-star-o').removeClass('fa-star-o').addClass('fa-star');
                }
            });
        }

		 var mref = at;
         var media_infavori = false;

         for (i = 0; i < tab_fav.length ; i++) {
				if ( 'ATLAS'+mref == tab_fav[i] ) {
                    media_infavori = true;
                }
         }

            if( mref.substring(0,2) == 'de' ) {
                mref+='&tx_eu[mrefo]='+$('.dropdown-menu-right li a').attr('href').replace('#','');
            }

            tx_eu_addAtlasForm('<xjxquery><q>tx_eu[mref]='+mref+'</q></xjxquery>');

			if (tab_fav.length>0 && media_infavori == true ) {

               //Onglet en francais
               if ( $('#add-atlas-fav').length ){
                   $('#add-atlas-fav  button').addClass('btn-universalis');
                }

           }
          	else {

          		$('#add-atlas-fav button').removeClass('btn-universalis');
          	}

		}
	}
}

var showLegend = function(map){
	$("#legends").find('.legende').addClass('hidden');
	$("#legends").find('.legende-'+map).removeClass('hidden');
	$("#legends").find('.legende-type').addClass('hidden');
	$("#legends").find('.legende-type-'+ entityType).removeClass('hidden');
}

var makeTitle = function(title){
	$("title").html("Planisphère : "+title+" - Cartes - Encyclopædia Universalis");
}

var showCountry = function(url, carte, nref, state){
	$("#atlas-error").hide().find("#atlas-error-content").html("");
	results = findInObject(lsMonde.concat(lsContinent,lsSubContinent,lsCountry,lsRegion), nref.toUpperCase());
	var jsonCountry;
	sNREF = nref.replace(/.$/,"1");
	sURL = url.replace(nref,sNREF).toLowerCase();

	// carte administrative speciale pour la France
	if(nref.toUpperCase().indexOf('AT00690') > -1){
		fURL = url.replace(nref,nref.replace(/.$/,"3")).toLowerCase();
		france = true;
	}else{
		france = false;
	}
	url = url.toLowerCase();
	// on recupere le nouveau drapeau si pas en cache
	if(first && dSVG == "" && drap != ""){
		getDrap(drap);
	}

	// on recupere la carte de situation si pas en cache
	if(sSVG == "" && $.inArray(nref,noSituation) == -1){
		$.get(sURL, function(d){
			sSVG = $(d)[0].firstChild;
		}).fail(function() {
			$("#atlas-error-content").html("carte situation introuvable sur le serveur");
			$("#atlas-error").show();
		});
	}
	// on recupere la carte administrative de la France si pas en cache
	if(france && fSVG == ""){
		$.get(fURL, function(d){
			fSVG = $(d)[0].firstChild;
		}).fail(function() {
			$("#atlas-error-content").html("carte administrative introuvable sur le serveur");
			$("#atlas-error").show();
		});
	}
	// on recupere la carte complete si pas en cache
	if(svg == ""){
		$.get(url, function(data) {
			svg = $(data)[0].firstChild;

			$("#atlas-loading").hide();
			$("#atlas-map").html(svg);
			svgSize = svgCalculateSize(svg);
			if(svgSize.width > svgSize.height){
				svgMode = "landscape";
			}else{
				svgMode = "portrait";
			}
			// on désactive le bouton de zoom out si zoom minimum
			/*if(panzoomOpts.minScale == ratioScreen){
				$("#zoom-out").prop('disabled','disabled')
			}*/

			// on charge la carte au bon format
			selectMap(carte);
		}).fail(function() {
			$("#atlas-error-content").html("carte complète introuvable sur le serveur");
			$("#atlas-error").show();
		});
	}else{
		// on charge la carte au bon format
		selectMap(carte);
	}
	if(!first){
		$(".breadcrumb").html('<li><i class="fa fa-circle-o-notch fa-spin text-muted"></i></li>');
		$("#maps-loader").show();
		$("#tab-maps").find(".row").hide();
		$.get(results[0].url+"json/", function(data) {
			switch(data.current_element.attributes.type){
				case 'monde':
					entityType = "m";
				break;
				case 'continent':
					entityType = "c";
				break;
				case 'sous-ensemble continental':
					entityType = "sc";
				break;
				case 'pays':
					entityType = "p";
				break;
				default:
					entityType = "r";
			}
			if(dom.indexOf(data.current_element.attributes.id) > -1)
				entityType = "dom";

			historique.url = results[0].url;
			historique.title = data.current_element.current_element_name;
			historique.type = "atlas";

			/** stats piwik **/
			statsPiwik(historique.url, historique.title, window.location.href);
			/** EOF stats piwik **/
			saveURL(historique);

			makeTitle(data.current_element.current_element_name);
			data.breadcrumb = makeBreadCrumb(data);
			current = data.current_element.attributes.id;

			drap = data.current_element.drapeau.id;
			if(drap.indexOf('DE') > -1){
				getDrap(drap);
			}else{
				delete(data.current_element.drapeau);
			}

			// on fabrique les labels des différentes cartes
			for(i = 0; i < data.atlas_cartes.atlas_carte.length; i++){
				if(typeof mapLetters[i] !=="undefined"){
					v = data.atlas_cartes.atlas_carte[i].attributes.id.slice(-1);
					$("img.carte"+(i+1)).parent().attr('data-carte',nref.toLowerCase().slice(0, -1)+(i+1));
					data.atlas_cartes.atlas_carte[i].attributes.map = data.atlas_cartes.atlas_carte[i].attributes.id.toLowerCase();
					data.atlas_cartes.atlas_carte[i].attributes.title = mapTitles[(v-1)];
					data.atlas_cartes.atlas_carte[i].attributes.letter = mapLetters[(v-1)];
					if(v == 5 || v == 6){
						data.atlas_cartes.atlas_carte[i].attributes.isedu = true;
					}
				}
			}
			$("#maps-loader").hide();
			$("#tab-maps").find(".row").fadeIn();

			// cas particulier du drapeau
			if(typeof data.current_element.drapeau !== "undefined" && data.current_element.drapeau.id != "" ){
				data.current_element.drapeau.file = data.current_element.drapeau.id.toLowerCase()+".jpg";
				$("img.carteDrap").parent().attr('data-carte',data.current_element.drapeau.id.toLowerCase());
				$(".legende-D").find('p').html(data.current_element.drapeau.content.trim());
			}
			// on positione le split pour le colonnage + extraction des notes
			if(typeof data.country_details.country_detail !== "undefined"){
				$("#atlas-tab-chiffres, .bloc-situation, #atlas-sources").removeClass('hidden');
				cptDetails = data.country_details.country_detail.length-1;
				if(data.country_details.country_detail[cptDetails].country_label.indexOf("Note") > -1){
					data.country_details.note = data.country_details.country_detail[cptDetails];
					data.country_details.note.country_value = data.country_details.note.country_value.replace('. <strong>','. <br /><br /><strong>');
					data.country_details.country_detail = data.country_details.country_detail.slice(0,-1);
					pos = Math.ceil((cptDetails-1)/2);
				}
				else
					pos = Math.ceil(cptDetails/2);
				data.country_details.country_detail[pos].divided = true;
			}else{
				$("#atlas-tab-chiffres, .bloc-situation, #atlas-sources").addClass('hidden');
			}


			$("h1").html(data.current_element.current_element_name);

			optTemplates = [
				{
					'target':'#tab-maps .row',
					'template': cartesDrawer
				},
				{
					'target':'.breadcrumb',
					'template': breadcrumb
				},
				{
					'target':'#cartes-list',
					'template': cartes
				},
				{
					'target':'.bloc-situation .panel-body',
					'template': details
				},
				{
					'target':'#chiffres-tab',
					'template': detailsTab
				},
				{
					'target':'#links-list',
					'template': linksTab
				},
				{
					'target':'#notes',
					'template': notes
				},
				{
					'target':'.bloc-limitrophe .panel-body ul',
					'template': limitrophes
				},
				{
					'target':'#evenement',
					'template': evenement
				}
			];
			applyTemplate(optTemplates, data);
			if(data.current_element.iso != "")
				$("#toDataPays").attr('href','datapays/?c='+data.current_element.iso);

			if(!hasFav){
				$("#evenement").find('.linkAddFav').addClass('hidden');
			}
			selectMap(carte);
			title = $("[data-action=toggle-map].active").find('img').data('title');
			subtitle = $("[data-action=toggle-map].active").find('img').data('subtitle');
			$(".atlas-tab-header").find('h3').html(title +"<br />"+subtitle);
		})
	}

	if(carte != "D"){
		var hash = nref.replace(/.$/,parseInt(mapLetters.indexOf(carte)+1));
		title = results[0].name;
		urlState = results[0].url;
	}
	else{
		var hash = nref;
		title = "Drapeau national";
		urlState = window.location.href;
	}

	if(state && carte != "D")
		navigation({nref: nref, title: title, carte: carte, url: urlState+"#"+hash, hash: hash});

	if(carte == "D"){
		$("#a-addFav").attr('data-nref',drap.toUpperCase());
		$("#a-addFav").attr('data-url',urlState+"#"+drap.toUpperCase());
	}
	else{
		$("#a-addFav").attr('data-nref',nref);
		$("#a-addFav").attr('data-url',urlState+"#"+hash);
	}
	$("#a-addFav").attr('data-titre',$(".atlas-tab-header").find('h3').text());
}

$(function() {
	// highlight menu
	if(isMobile)
		$(".navbar-nav").find("a[href='/atlas/']").closest('li').addClass('active');

	if(isMobile && isConnected){
		$('[data-toggle="tooltip"]').tooltip("disable");
	}

	//if($(".dropdown-menu").find("*[data-action='favori']").length > 0)
	if($("*[data-action='favori']").length > 0)
		hasFav = true;

	$("<br />").insertBefore(".notes strong:not(:first-child)");
	makeTitle($("h1").text());
	// live search
	lsAll = [];
	lsAll = lsMonde.concat(lsCountry,lsSubContinent,lsRegion,lsContinent);
	var lsAll = lsAll.filter(function(value){if(Object.keys(value).length !== 0) return value});
	for(i = 0; i < lsAll.length; i++){
		if(lsAll[i].name == "")
			delete lsAll[i];
	}
	lsAll = unique(lsAll);
	var tagStart = '<span class="found">';
	var tagEnd = '</span>';
	var tagOffset = tagStart.length;
	$("#search-atlas").keyup(function(e){
		val = $(this).val();
		if(val.length > 2){
			content = '<ul class="list-unstyled">';
				index = objectFindByKey(lsAll,'name',val);
			cpt = index.length;
			if(cpt > 0){
				$("#live-result").removeClass('hidden');
				for(i = 0; i < cpt; i++){
					name = insertIntoString(tagStart,lsAll[index[i][0]].name,index[i][1]);
					name = insertIntoString(tagEnd,name,parseInt(tagOffset+index[i][1]+val.length));
					content +='<li class="item"><a href="'+lsAll[index[i][0]].url+'"><i class="fa fa-caret-right"></i> '+name+'</a></li>';
				}
			}
			content += "</ul>";
			$("#live-result").html(content);
			if($("#live-result .item").length > 0)
				$("#live-result .item").first().addClass('active');
			else
				$("#live-result").addClass('hidden');
		}else{
			$("#live-result").addClass('hidden');
		}
	});
	$(document).click(function(e){
		if(!$(e.target).closest('#live-result').length) {
			if(!$('#live-result').hasClass('hidden')) {
				$('#live-result').addClass('hidden');
			}
		}
	});

	$("body").keydown(function(e) {
		if(!$("#live-result").hasClass('hidden')){
			switch(e.keyCode){
				case 27: // escape
					$("#live-result").addClass('hidden');
					$("#search-atlas").blur();
				break;
				case 38: // arrow up
					e.preventDefault();
					if( $("#live-result .item").length > 1){
						$("#search-atlas").blur();
						var selected = $("#live-result .active");
						pos = $("#live-result .active").index();
							$("#live-result li").removeClass("active").blur();
						if(pos == 1) {
							selected.siblings(".item").last().addClass("active").focus();
						}else if(selected.prev().hasClass('header')){
							selected.prev().prev(".item").addClass("active").focus();
						}else{
							selected.prev(".item").addClass("active").focus();
						}
					}
					return true;
				break;
					case 40: // arrow down
					e.preventDefault();
					if( $("#live-result .item").length > 1){
						$("#search-atlas").blur();
						var selected = $("#live-result .active");
						pos = $("#live-result .active").index()-$("#live-result .header").length+1;
						$("#live-result li").removeClass("active").blur();
						if($(".item").length == pos) {
							selected.siblings(".item").first().addClass("active").focus();
						}else if(selected.next().hasClass('header')){
							selected.next().next(".item").addClass("active").focus();
						}
						else {
							selected.next(".item").addClass("active").focus();
						}
					}
					return true;
				break;

				case 13: // enter
					if($("#live-result li").is(":focus")){
						window.location = $("#live-result li:focus").find("a").attr('href');
						}if($("#live-result li").hasClass('active')){
						window.location = $("#live-result li.active").find("a").attr('href');
					}
				break;
					default:
					$("#search-atlas").focus();
			}
		}
	});
	// EOF live search

	initTemplates();

	panzoom = $("#atlas-map").panzoom(panzoomOpts);
	panzoom.parent().on('mousewheel.focal', function( e ) {
		if(typeof e.target.className === "object"){
			e.preventDefault();
			var delta = e.delta || e.originalEvent.wheelDelta;
			var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
			panzoom.panzoom('zoom', zoomOut, {
				animate: false,
				focal: e
			});
		}
	});
	panzoom.on('panzoomzoom',function(e, panzoom, scale, opts){
		if(scale == opts.maxScale){
			$("#zoom-in").prop('disabled','disabled');
		}else{
			$("#zoom-in").prop('disabled',false);
		}
		if(scale == opts.minScale){
			$("#zoom-out").prop('disabled','disabled');
		}else{
			$("#zoom-out").prop('disabled',false);
		}
	});
	panzoom.on('panzoomend', function( e, panzoom, matrix, changed ) {
		var a = 'nope';
		if(!changed){
			if((e.target.localName == "tspan" || e.target.localName == "text") && (typeof e.target.dataset['nref'] !== "undefined")){
				a = e.target.getAttribute('data-nref');
			}else if(e.target.parentNode.localName == "tspan"){
				a = e.target.parentNode.parentNode.getAttribute('data-nref');
			}
			else if(e.target.localName == "tspan"){
				a = e.target.parentNode.getAttribute('data-nref');
			}
			if(a.trim() != "nope" && a.trim() != current && a != "null"){
				loadingMap();
				var carte = $("*[data-action=toggle-map].active").data('value');
				var original = $("*[data-action=toggle-map].active").data('carte');
				url = urlSVG+a+".svg";
				showCountry(url, carte, a, true);
			}
		}
	});

	$(document).on('click','*[data-recherche]',function(e){
		window.location.href = "/recherche/q/"+$(this).data('recherche')+"/";
	})
	$(".atlas-tab-close").on('click',function(e){
		e.preventDefault();
		$(".atlas-tab-container").removeClass('atlas-tab-opened');
		$(".atlas-tab-menu").find('.list-group-item.active').removeClass('active');
	});

	$("div.atlas-tab-menu>div.list-group>a").click(function(e) {
        e.preventDefault();
        if($(this).hasClass('active')){
			//$(".atlas-tab-close").trigger('click');
			$(".atlas-tab-container").removeClass('atlas-tab-opened');
			$(".atlas-tab-menu").find('.list-group-item.active').removeClass('active');
			return false;
        }
        if(!$(".atlas-tab-container").hasClass('atlas-tab-opened'))
        	$(".atlas-tab-container").addClass('atlas-tab-opened');
        $(this).siblings('a.active').removeClass("active");
        $(this).addClass("active");
        var index = $(this).index();
        $("div.atlas-tab>div.atlas-tab-content").removeClass("active");
        $("div.atlas-tab>div.atlas-tab-content").eq(index).addClass("active");
    });

	// click sur la landing atlas
	$(document).on('click',"*[data-toggle=atlas]",function(e){
		$("body").addClass('no-scroll');
		$("#modal-atlas").fadeIn();
		var carte = $(this).data('carte');
		url = urlSVG+$(this).data('nref').toUpperCase()+".svg";
		$("#cartes").attr('data-media',$(this).data('nref').toUpperCase());
		showCountry(url, carte,$(this).data('nref').toUpperCase(), true); //, $(this).data('position').replace('cat','AT')
	});

	$(document).on('click','#modal-atlas .breadcrumb a', function(e){
		e.preventDefault();
		nref = $(this).data('nref');
		carte = $("#tab-maps").find('[data-action=toggle-map].active').data('value');
		state = true;
		urlM = urlSVG+nref+".svg";
		loadingMap();
		showCountry(urlM, carte, nref, state);
	});

	// click dans le tiroir de cartes
	$(document).on('click','*[data-action=toggle-map]',function(e){
		e.preventDefault();
		map = $(this).data('value');
		nref = $(this).data('carte');
		switch(map){
			case 'A':
				if(france){
					$("#atlas-map").html(fSVG);
				}else{
					$("#atlas-map").html(svg);
				}
			break;
			case 'S':
				$("#atlas-map").html(sSVG);
			break;
			case 'D':
				$("#atlas-map").html(dSVG);
			break;
			default:
				$("#atlas-map").html(svg);
		}

		$("*[data-action=toggle-map]").removeClass('active');
		$(this).addClass('active');
		showLegend(map);
		$("*[data-type=carte]").hide();
		$("*[data-map-"+map.toLowerCase()+"=true]").show();
		title = $(this).find('img').data('title');
		subtitle = $(this).find('img').data('subtitle');
		$(".atlas-tab-header").find('h3').html(title +"<br />"+subtitle);
		$("#links-list").find('ul').hide();
		$("#links-"+nref).show();
		if(isMobile){
			$(".atlas-tab-close").trigger('click');
		}
		if(typeof nref !== "undefined" && !nref.startsWith('DE')){
			$("#a-addFav").show();
			$("#a-addFav").attr('data-nref',nref);
			url = window.location.href.split('#')[0]+"/#"+nref;
			$("#a-addFav").attr('data-url',url);
			$("#a-addFav").attr('data-titre',$(".atlas-tab-header").find('h3').text());
		}else{
			$("#a-addFav").hide();
			$("#atlas-tab-legend").trigger('click');
		}
	})

	$(".atlas-close").on('click',function(e){
		$("body").removeClass('no-scroll');
		$("#modal-atlas").fadeOut();
		$(".atlas-tab-container").removeClass('atlas-tab-opened');
		$(".atlas-tab-menu").find('.list-group-item.active').removeClass('active');
		navigation({nref:null, title: "Planisphère", url: window.location.href.split("#")[0]})
		first = true;
	})

	$("[data-action=print-atlas]").on('click',function(e){
		e.preventDefault();
		// before
		$("#modal-atlas").removeClass('hidden-print');
		$("#atlas-main, #medias-fr, #favoris_historique").addClass('hidden-print');
		$("#modal-atlas").after('<div id="print-legend"><h3>Légende</h3>'+$(".legende:not(.hidden)").html()+'</div>');
		window.print();
		// after
		$("#print-legend").remove();
		$("#modal-atlas").addClass('hidden-print');
		$("#atlas-main, #medias-fr, #favoris_historique").removeClass('hidden-print');
	})

	$("#callSommaire").on('click',function(e){
		e.preventDefault();
		$(".sommaire").css('margin-top','0')
	});
	$("[data-action='closeSomm']").on('click',function(e){
		e.preventDefault();
		$(".sommaire").css('margin-top','-1000');
	})

	if(window.location.hash !== ""){
		h = window.location.hash.split('#').pop();
		$("[data-position=c"+h.toLowerCase()+"]").trigger('click');
	}
});

/*********************************/
/*            ATLAS              */
/*********************************/
	if($("#atlas-container").length > 0){
		var hash = window.location.href.split("#").pop().toLowerCase();

		if(hash == "chiffres" && isDesktop || (hash == "chiffres" && isTablet && $("html").hasClass('landscape'))){
			$('html,body').animate({
				scrollTop: $("#chiffres").offset().top
			},500);
		}
		if(hash == "chiffres" && (isMobile || (hash == "chiffres" && isTablet && $("html").hasClass('portrait')))){

			$("#details-mobile").modal('show');
		}
		if(hash.indexOf("http") == -1 && hash != "chiffres"){
			showLegend = $("a[href=#"+hash+"]").data('legend');
			media = hash+".jpg";
			atlas_player("",media,"fr",showLegend);
		}

		$("<br />").insertBefore(".notes strong:not(:first-child)");
		$(".bloc-situation dd sup").each(function(){
			content = $(this).text().replace(' ','');
			if(!isNaN(content)){
				$(this).html('<a href="#" class="anchor">'+content+'</a>');
			}
		});
		$("dd a.anchor").on('click',function(e){
			e.preventDefault();
			$('html,body').animate({
				scrollTop: $("#notes").offset().top
			},500);
		});

		$("#navigation a[data-action=tree]").on('click',function(e){
			e.preventDefault();
			id = $(this).attr("href");
			if($(this).find('.fa-folder').length > 0){
				$(id).slideDown();
				$(this).find('i').removeClass('fa-folder').addClass('fa-folder-open');
			}else{
				$(id).slideUp();
				$(this).find('i').removeClass('fa-folder-open').addClass('fa-folder');
			}
		});
		/** live search **/
		countryAll = unique(countryAll);
		regionMetroAll = unique(regionMetroAll);
		regionOutAll = unique(regionOutAll);

		var tagStart = '<span class="found">';
		var tagEnd = '</span>';
		var tagOffset = tagStart.length;

		$("#search-atlas").keyup(function(e){
			val = $(this).val();
			if(val.length > 2){
				content = '<ul class="nav nav-pills nav-stacked text-left">';

				index = objectFindByKey(subContinentAll,'name',val);
				cpt = index.length;
				// subcontinents
				if(cpt > 0){
					$("#live-result").removeClass('hidden');
					if(cpt > 0)
						content += '<li class="header">Sous-ensembles continentaux</li>';
					for(i = 0; i < cpt; i++){
						name = insertIntoString(tagStart,subContinentAll[index[i][0]].name,index[i][1]);
						name = insertIntoString(tagEnd,name,parseInt(tagOffset+index[i][1]+val.length));

						content +='<li class="item"><a href="'+subContinentAll[index[i][0]].url+'"><i class="fa fa-chevron-right"></i> '+name+'</a></li>';
					}
				}

				// countries
				index = objectFindByKey(countryAll,'name',val);
				cpt = index.length;
				if(cpt > 0){
					$("#live-result").removeClass('hidden');
					if(cpt > 0)
						content += '<li class="header">Pays et entités secondaires</li>';
					for(i = 0; i < cpt; i++){
						name = insertIntoString(tagStart,countryAll[index[i][0]].name,index[i][1]);
						name = insertIntoString(tagEnd,name,parseInt(tagOffset+index[i][1]+val.length));

						content +='<li class="item"><a href="'+countryAll[index[i][0]].url+'"><i class="fa fa-globe"></i> '+name+'</a></li>';
					}
				}

				// regions metropolitaine
				index = objectFindByKey(regionMetroAll,'name',val);
				cpt = index.length;
				if(cpt > 0){
					$("#live-result").removeClass('hidden');
					if(cpt > 0)
						content += '<li class="header">France métropolitaine</li>';
					for(i = 0; i < cpt; i++){
						name = insertIntoString(tagStart,regionMetroAll[index[i][0]].name,index[i][1]);
						name = insertIntoString(tagEnd,name,parseInt(tagOffset+index[i][1]+val.length));

						content +='<li class="item"><a href="'+regionMetroAll[index[i][0]].url+'"><i class="fa fa-caret-right"></i> '+name+'</a></li>';
					}
				}

				// regions outremer
				index = objectFindByKey(regionOutAll,'name',val);
				cpt = index.length;
				if(cpt > 0){
					$("#live-result").removeClass('hidden');
					if(cpt > 0)
						content += '<li class="header">France d\'outre-mer</li>';
					for(i = 0; i < cpt; i++){
						name = insertIntoString(tagStart,regionOutAll[index[i][0]].name,index[i][1]);
						name = insertIntoString(tagEnd,name,parseInt(tagOffset+index[i][1]+val.length));

						content +='<li class="item"><a href="'+regionOutAll[index[i][0]].url+'"><i class="fa fa-caret-right"></i> '+name+'</a></li>';
					}
				}

				content += "</ul>";

				$("#live-result").html(content);

				if($("#live-result .item").length > 0)
					$("#live-result .item").first().addClass('active');
				else
					$("#live-result").addClass('hidden');
			}else{
					$("#live-result").addClass('hidden');
			}
		});

		$(document).click(function(e){
			if(!$(e.target).closest('#live-result').length) {
				if(!$('#live-result').hasClass('hidden')) {
					$('#live-result').addClass('hidden');
				}
			}
		});

		$("body").keydown(function(e) {
			if(!$("#live-result").hasClass('hidden')){
				switch(e.keyCode){
					case 27: // escape
						$("#live-result").addClass('hidden');
						$("#search-atlas").blur();
					break;
					case 38: // arrow up
						e.preventDefault();
						if( $("#live-result .item").length > 1){
							$("#search-atlas").blur();
							var selected = $("#live-result .active");
							pos = $("#live-result .active").index();

							$("#live-result li").removeClass("active").blur();
							if(pos == 1) {
								selected.siblings(".item").last().addClass("active").focus();
							}else if(selected.prev().hasClass('header')){
								selected.prev().prev(".item").addClass("active").focus();
							}else{
								selected.prev(".item").addClass("active").focus();
							}
						}
						return true;
					break;

					case 40: // arrow down
						e.preventDefault();
						if( $("#live-result .item").length > 1){
							$("#search-atlas").blur();
							var selected = $("#live-result .active");
							pos = $("#live-result .active").index()-$("#live-result .header").length+1;
							$("#live-result li").removeClass("active").blur();
							if($(".item").length == pos) {
								selected.siblings(".item").first().addClass("active").focus();
							}else if(selected.next().hasClass('header')){
								selected.next().next(".item").addClass("active").focus();
							}
							else {
								selected.next(".item").addClass("active").focus();
							}
						}
						return true;
					break;

					case 13: // enter
						if($("#live-result li").is(":focus")){
							window.location = $("#live-result li:focus").find("a").attr('href');

						}if($("#live-result li").hasClass('active')){
							window.location = $("#live-result li.active").find("a").attr('href');
						}
					break;

					default: // pour continuer la recherche
						$("#search-atlas").focus();
				}
			}
		});
		/** EOF live search **/

		// mode mobile
		if(window.innerWidth < 767){
			$(".media-element").css('height',window.innerHeight - $(".media-extra").height()-30)
		}
		$(window).on('resize',function(e){
			if(window.innerWidth < 767){
				$(".media-element").css('height',window.innerHeight - $(".media-extra").height()-30)
			}else{
				$(".media-element").removeAttr('style');
			}
		})
	}

	$("*[data-toggle=atlas] a").on('click',function(e){
		e.preventDefault();
		hash = $(this).attr('href').split("#").pop().toLowerCase();
		showLegend = $("a[href=#"+hash+"]").data('legend');
		media = hash+".jpg";
		atlas_player("",media,"fr",showLegend);
	});