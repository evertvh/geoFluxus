define(['utils/session'],
function (Session) {

    /**
    * global configuration file
    * @module config
    *
    * @author Christoph Franke
    */
    var config = {
        URL: '/' // base application URL
    };

    config.session = new Session();


    config.views = {
        layerproxy: '/proxy/layers/{0}/wms',
    }

    /** urls to resources in api
    * @name api
    * @memberof module:config
    */
    config.api = {
        base:                   '/api', // base Rest-API URL
        casestudies:            '/api/casestudies/',
        publications:           '/api/publications/',
        publicationsInCasestudy:'/api/casestudies/{0}/publications/',
        products:               '/api/products/',
        wastes:                 '/api/wastes/',
        keyflows:               '/api/keyflows/',
        qualities:              '/api/qualities/',
        reasons:                '/api/reasons/',
        targets:                '/api/casestudies/{0}/targets',
        targetvalues:           '/api/targetvalues',
        targetspatialreference: '/api/targetspecialreference/',
        impactcategories:       '/api/impactcategories/',
        units:                  '/api/units/',
        challenges:             '/api/casestudies/{0}/challenges',
        aims:                   '/api/casestudies/{0}/aims',
        chartCategories:        '/api/casestudies/{0}/chartcategories/',
        charts:                 '/api/casestudies/{0}/chartcategories/{1}/charts/',
        stakeholderCategories:  '/api/casestudies/{0}/stakeholdercategories/',
        stakeholders:           '/api/casestudies/{0}/stakeholdercategories/{1}/stakeholders/',
        solutionCategories:     '/api/casestudies/{0}/solutioncategories/',
        solutions:              '/api/casestudies/{0}/solutioncategories/{1}/solutions/',
        solutionQuantities:     '/api/casestudies/{0}/solutioncategories/{1}/solutions/{2}/solutionquantities',
        solutionRatioOneUnits:  '/api/casestudies/{0}/solutioncategories/{1}/solutions/{2}/solutionratiooneunits',
        implementations:        '/api/casestudies/{0}/implementations/',
        solutionsInImplementation: '/api/casestudies/{0}/implementations/{1}/solutions/',
        quantitiesInImplementedSolution: '/api/casestudies/{0}/implementations/{1}/solutions/{2}/quantities',
        layerCategories:        '/api/casestudies/{0}/layercategories',
        layers:                 '/api/casestudies/{0}/layercategories/{1}/layers',
        keyflowsInCaseStudy:    '/api/casestudies/{0}/keyflows',
        activitygroups:         '/api/casestudies/{0}/keyflows/{1}/activitygroups/',
        activities:             '/api/casestudies/{0}/keyflows/{1}/activities/',
        actors:                 '/api/casestudies/{0}/keyflows/{1}/actors/',
        adminLocations:         '/api/casestudies/{0}/keyflows/{1}/administrativelocations/',
        opLocations:            '/api/casestudies/{0}/keyflows/{1}/operationallocations/',
        materials:              '/api/casestudies/{0}/keyflows/{1}/materials/',
        activityToActivity:     '/api/casestudies/{0}/keyflows/{1}/activity2activity/',
        groupToGroup:           '/api/casestudies/{0}/keyflows/{1}/group2group/',
        actorToActor:           '/api/casestudies/{0}/keyflows/{1}/actor2actor/',
        groupStock:             '/api/casestudies/{0}/keyflows/{1}/groupstock/',
        activityStock:          '/api/casestudies/{0}/keyflows/{1}/activitystock/',
        actorStock:             '/api/casestudies/{0}/keyflows/{1}/actorstock/',
        flowIndicators:         '/api/casestudies/{0}/keyflows/{1}/flowindicators/',
        arealevels:             '/api/casestudies/{0}/levels/',
        areas:                  '/api/casestudies/{0}/levels/{1}/areas/',
        wmsresources:           '/api/casestudies/{0}/wmsresources/'
    };

    return config;
}
);
