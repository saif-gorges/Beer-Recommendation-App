// Recommendation A

// dropdown menu
let dropdownMenuB = d3.select("#select-beer")

// d3.csv('static/beer_score.csv').then(data => {
   
//     // List of Beers
//     let beerList = data.beer_name

//     // Test
//     console.log(beerList)

//     // Populate dropdowns selections
//     beerList.forEach ( beer => dropdownMenu.append("option").text(beer) );
    
// });

let beerList = ["San Miguel", "Newcastle Brown Ale (Non-US Version)", "Rickard's Red", "Paradox Beer Candid Kaiser - American Style Pale Ale",
"Maclay's Traditional Pale Ale", "Carlsberg Pilsner", "Weihenstephaner Hefeweissbier", "Mill Street Original Organic Lager",
"Tatra Jasne Pelne / Pils / Beer", "Muskoka Cream Ale", "Samuel Smiths Organic Lager", "Cool Beer Blonde Lager",
"Berthold Keller Premium Lager", "Creemore Springs Premium Lager", "Erdinger Weissbier", "Harp Lager",
"Paulaner Oktoberfest Bier (Wiesn Bier)", "Great Lakes Brewery Canuck Pale Ale", "DAB Original", "Pilsner Urquell",
"Guinness Draught", "Tsingtao Beer Quality Series (Taiwan)", "Stella Artois", "Bud Light", "Heineken", "Michelob Ultra",
"Waterloo IPA", "Goose Island IPA Now", "Alexander Keith's India Pale Ale", "Kozel CernÃ½ (Dark)", "Chang Beer",
"Kona Big Wave Golden Ale", "Beck's", "Budweiser", " Hoegaarden RosÃ©e", "MacKinnon Brothers Red Fox", "Corona Extra",
"Maisel & Friends Marc's Chocolate Bock", "Krombacher Pils", "BrewDog / Weihenstephan India Pale Weizen", "Flying Monkeys 12 Minutes to Destiny",
"Steam Whistle Pilsner", "Peroni", "Tiger Beer", "Moosehead Pale Ale", "Sleeman Clear 2.0", "Zubr", "Baltika 7 Eksportnoe (Export)",
"Midnight Sun M", "Toppling Goliath Kentucky Brunch", "Superstition Berry White", "NÃƒÂ¤rke Kaggen Stormaktsporter",
"Bavaria 8.6 (Original)", "The Twisted Hop Tears... in Rain: Glitter in the Dark", "Bud Light Apple", "Bud Light Lime",
"Boxer Ice", "Molson Carling Light", "Estrella Damm (5.4%)", "Cantillon Vin Jaune", "Dos Equis XX Special Lager",
"Dragon Stout", "Innis & Gunn The Original", "Kirin Ichiban", "Mad Jack Apple Lager", "Mickeys Fine Malt Liquor",
"Old Milwaukee", "Bellwoods Jelly King (Raspberry and Blackberry)", "Unibroue La Fin du Monde", "Sapporo Premium Beer / Draft Beer",
"Wissey Valley Golden Rivet", "Caledon Hills Helles", "Wellington Special Pale Ale SPA", "Kronenbourg 1664 Blanc",
"Smithwick's Ale / Draught", "Nickel Brook Glory & Gold", "Miller Lite", "Shawn & Ed Lagershed Original", "Walkerville Classic Amber Lager",
"Muskoka Mad Tom IPA", "Four Winds Nectarous", "Dieu du Ciel! PÃ©chÃ© Mortel (Bourbon)", "Driftwood Sartori Harvest IPA",
"Unibroue Trois Pistoles", "Bellwoods Bring Out Your Dead", "Driftwood Fat Tug IPA", "Hoegaarden Grand Cru",
"Unibroue 17 Grande RÃ©serve (Rhum & Cognac)"]

beerList.forEach( beer => dropdownMenuB.append("option").text(beer) );


// Factors
let factors = ["Flavor", "Aroma", "Mouthfeel"]

// Dropdown Menu
let dropdownMenuT = d3.select("#select-taste")

factors.forEach( factor => dropdownMenuT.append("option").text(factor) );


///////////// Recommendation B //////////////////

let dropdown1B = d3.select("#select-beer1")
let dropdown1R = d3.select("#rate-beer1")

let dropdown2B = d3.select("#select-beer2")
let dropdown2R = d3.select("#rate-beer2")

let dropdown3B = d3.select("#select-beer3")
let dropdown3R = d3.select("#rate-beer3")

let dropdown4B = d3.select("#select-beer4")
let dropdown4R = d3.select("#rate-beer4")

let dropdown5B = d3.select("#select-beer5")
let dropdown5R = d3.select("#rate-beer5")

rateList = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

beerList.forEach( beer => dropdown1B.append("option").text(beer) );
beerList.forEach( beer => dropdown2B.append("option").text(beer) );
beerList.forEach( beer => dropdown3B.append("option").text(beer) );
beerList.forEach( beer => dropdown4B.append("option").text(beer) );
beerList.forEach( beer => dropdown5B.append("option").text(beer) );

rateList.forEach( rating => dropdown1R.append("option").text(rating) );
rateList.forEach( rating => dropdown2R.append("option").text(rating) );
rateList.forEach( rating => dropdown3R.append("option").text(rating) );
rateList.forEach( rating => dropdown4R.append("option").text(rating) );
rateList.forEach( rating => dropdown5R.append("option").text(rating) );

