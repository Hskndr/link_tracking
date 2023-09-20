javascript:(function() {
    /*Cambia esto al dominio que deseas rastrear*/
    var targetDomain = "www.eada.edu"; 
    /*Para evitar bucles infinitos*/
    var visitedLinks = {}; 
    var matchingLinks = [];
    console.log("1");
    
    function findLinksRecursive(url) {
      if (visitedLinks[url]) {
        return;
      }
  
      visitedLinks[url] = true;
  
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var parser = new DOMParser();
          var doc = parser.parseFromString(xhr.responseText, "text/html");
          var links = doc.getElementsByTagName("a");
  
          for (var i = 0; i < links.length; i++) {
            var link = links[i];
            if (link.href.indexOf(targetDomain) !== -1) {
              matchingLinks.push(link.href);
            }
          }
  
          for (var i = 0; i < links.length; i++) {
            var link = links[i];
            if (link.href.indexOf(targetDomain) !== -1) {
              findLinksRecursive(link.href);
            }
          }
        }
      };
  
      xhr.open("GET", url, true);
      xhr.send();
    }
  
    findLinksRecursive(window.location.href);

    console.log("2",findLinksRecursive(window.location.href));

    setTimeout(function() {
      if (matchingLinks.length > 0) {
        alert("Enlaces asociados a " + targetDomain + ":\n\n" + matchingLinks.join("\n"));
      } else {
        alert("No se encontraron enlaces asociados a " + targetDomain + " en esta página.");
      }
    }, 5000); /*Espera 5 segundos para asegurarse de que todas las solicitudes se completen*/
  
})();
  