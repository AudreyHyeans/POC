/** FORMULAIRE DE RECHERCHE **/
	var engine = "solr"; // lucene
	function displayLiveSearch(obj){
		var source = obj.source;
		var target = obj.target;
		var classes = obj.classes;
		var url = obj.url;
		var val = $(source).val();
		var urlSearch = "/recherche/l/1/q/";

		if(engine == "lucene")
			urlSearch = "/recherche/l/1/napp/";

		if($("#"+target).length == 0){
			$(source).after('<div id="'+target+'" class="'+classes+' hidden"></div>');
		}
		if(val.length > 2){
			var ajax = new XMLHttpRequest();
			ajax.onload = function() {
				var results = JSON.parse(ajax.responseText);
				if(results.length > 0){
					var contentLiveSearch = '<ul class="list-unstyled">';
					JSON.parse(ajax.responseText).map(function(i) {
						sTerm = i.label;
						if(engine == "lucene")
							sTerm = i.id;

						contentLiveSearch += '<li class="item"><a href="'+encodeURI(urlSearch+sTerm)+'">'+i.value+'</a></li>';
					});

					contentLiveSearch += '</ul>';
					$("#"+target).html(contentLiveSearch);
					$("#"+target).removeClass('hidden');
				}else{
					$("#"+target).addClass('hidden');
				}
			};
			ajax.open("GET", url+val, true);
			ajax.send();
		}else{
			$("#"+target).addClass('hidden');
		}
	}

	$("body").keydown(function(e) {
		if($("#live-search-desktop").is(':visible')){
			switch(e.keyCode){
				case 27: // escape
					$("#live-search-desktop").addClass('hidden');
				break;
				case 38: // arrow up
					e.preventDefault();
					if($("#live-search-desktop .item").length > 1){
						var selected = $("#live-search-desktop .active");
						pos = $("#live-search-desktop .active").index();
						$("#live-search-desktop li").removeClass("active").blur();
						if(pos == -1){
							$("#live-search-desktop .item").last().addClass("active").focus();
						}else if(pos == 0) {
							selected.siblings(".item").last().addClass("active").focus();
						}else{
							selected.prev(".item").addClass("active").focus();
						}
					}
					return true;
				break;
				case 40: // arrow down
				e.preventDefault();
				if( $("#live-search-desktop .item").length > 1){
					var selected = $("#live-search-desktop .active");
					pos = $("#live-search-desktop .active").index()+1;
					$("#live-search-desktop li").removeClass("active").blur();
					if(pos == 0){
						$("#live-search-desktop .item").first().addClass("active").focus();
					}
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
					$('#s-desktop').on('submit', function(event){
						if($("#live-search-desktop li").is(":focus")){
							window.location.href = $("#live-search-desktop li:focus").find("a").attr('href');
						}else if($("#live-search-desktop li").hasClass('active')){
							window.location.href = $("#live-search-desktop li.active").find("a").attr('href');
						}else{
							return true;
						}
				    });
				break;
			}
		}
	});
	if($("#search-desktop").length > 0 && (isEDU || isFR)){

		$("#search-desktop").on('keyup',function(e){
			var forbiddenKeys = [27,38,40];
			if(forbiddenKeys.indexOf(e.keyCode) == -1)
				displayLiveSearch({
					source: "#search-desktop",
					target: "live-search-desktop",
					classes: "live-search box-shadow arrow-box",
					url: "/index.php?eID=live_search&type=encyclopedie&term="
				});
		});
	}
	if($("#search-mobile").length > 0 && (isEDU || isFR)){
		$("#search-mobile").on('keyup',function(e){
			displayLiveSearch({
					source: "#search-mobile",
					target: "live-search-mobile",
					classes: "live-search-mobile",
					url: "/index.php?eID=live_search&type=encyclopedie&term="
				})
		});
	}