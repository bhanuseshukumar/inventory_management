function table_fun(){
    tab = document.getElementsByClassName("tab-hide")[0]
    if(tab != undefined)
    {
        tab.style.display = "table"
    }
}
document.body.addEventListener( 'load', table_fun, true );
