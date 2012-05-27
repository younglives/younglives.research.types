jq(document).ready(function() {
    jq('.facet_item').click(function() {
        document.facetSearch.submit();
    });
});
