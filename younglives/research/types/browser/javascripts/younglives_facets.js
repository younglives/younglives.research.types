jq(document).ready(function() {

    jq('.facet_item').click(function() {
        jq('#facetSearch').submit();
    });

});
