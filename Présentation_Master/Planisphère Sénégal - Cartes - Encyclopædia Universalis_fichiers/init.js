	var new_string = "";

	/** tableau general de toutes les lettres sans accents **/
	var total = new Array("a","c","d","e","g","h","i","j","k","l","n","o","r","s","t","u","w","y","z");

	/** tableaux contenant les caracteres accentues **/
	var a = new Array("à","â","ä","á","ã","å","ă","ā","ą");
	var c = new Array("ç","č","ć","ĉ","ċ");
	var d = new Array("ð","đ","ď");
	var e = new Array("è","ê","é","ë","ě","ė","ē","ę");
	var g = new Array("ǵ","ğ","ģ","ĝ","ġ");
	var h = new Array("ĥ","ħ");
	var i = new Array("ì","í","î","ï","İ","ī","ı","į","ĩ");
	var j = new Array("ĵ");
	var k = new Array("ķ","ĸ");
	var l = new Array("ĺ","ľ","ļ","l·","ł");
	var n = new Array("ñ","ń","ŋ","ŉ","ň","ņ");
	var o = new Array("ó","ô","ö","ò","ø","õ","ő","ō");
	var r = new Array("ŕ","ř","ŗ");
	var s = new Array("ß","ś","š","ş","ŝ");
	var t = new Array("ť","ţ","ŧ");
	var u = new Array("ú","û","ü","ù","ŭ","ű","ū","ų","ů","ũ");
	var w = new Array("ŵ");
	var y = new Array("ý","ÿ","ŷ");
	var z = new Array("ź","ž","ż");

	/** caracteres tres speciaux **/
	var autre = new Array("æ","œ","þ");
	var autre_replace = new Array("ae","oe","th");

	var $in = new Array();
	var $out = new Array();

	/** on parcours chaque tableau de chaque lettre sans accent (on joue avec des variables de variables !!) **/
	for ($total = 0; $total < total.length; $total ++){
		$temp  = total[$total];
		for($sub = 0; $sub < this[total[$total]].length; $sub ++){
			$in.push(this[total[$total]][$sub]);
			$out.push($temp);
		}
	}

	/** init des 2 tableaux pour les comparaisons **/
	var pattern_accent = $in.concat(autre);
	var pattern_replace_accent = $out.concat(autre_replace);


	/** emulation du preg_replace qui n'exsite pas en JS **/
	function preg_replace (array_pattern, array_pattern_replace, my_string)
	{

		var new_string = String (my_string);
		for (i=0; i<array_pattern.length; i++)
		{
			var reg_exp = RegExp(array_pattern[i], "gi");
			var val_to_replace = array_pattern_replace[i];
			new_string = new_string.replace (reg_exp, val_to_replace);
		}
		return new_string;
	}

	/** on applatit tous les caratecres **/
	function no_accent (my_string)
	{
		if (my_string && my_string!= "")
			new_string = preg_replace (pattern_accent, pattern_replace_accent, my_string);
		return new_string;
	}

	/** insertion du bloc highlight au bon endroit **/
	function insertIntoString(insertString, insertInto, position)
	{
		first = insertInto.substr(0,position);
		end = insertInto.substr(position);
		first = first+insertString;
		result = first+end;
		return result;
	}

Array.prototype.unique = function()
{
    var tmp = {}, out = [];
    for(var i = 0, n = this.length; i < n; ++i)
    {
        if(!tmp[this[i]]) { tmp[this[i]] = true; out.push(this[i]); }
    }
    return out;
}

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};