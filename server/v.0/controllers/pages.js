// Load dependency
var solr = require('solr-client');
var config = require("../../config")

var page_size = 20
// Create a client
var client = solr.createClient({
    host: config.solr_address,
    port: config.solr_port,
    core: config.solr_core
});

var i = {
    page: (req, res) => {
        try {
            var page = req.params["page"] | 1
            var query = req.query
            var f_query = "*"

            var search = "*:*"

            var q = {
                "fl": "*",
                "q": search,
                "fq": f_query,
                "start": (parseInt(page) - 1) * page_size
            }

            i.query_page(q, res)
        } catch (err) {
            res.status(500).json({
                err: err.message
            })
        }
    },
    query_page: (query, res) => {
        try {
            var fields = query["fl"]
            var q = query["q"]
            var fq = query["fq"]
            var start = query["start"]

            var query = client.createQuery()
                .q(q)
                .fq(fq)
                .fl(fields)
                .sort({})
                .start(start)
                .rows(page_size)

            console.log(query);

            client.search(query, function (err, result) {
                if (err) {
                    console.log(err);
                    return;
                }

                res.json({
                    ok: 1,
                    data: result.response
                })
            });
        } catch (err) {
            res.status(500).json({
                err: err.message
            })
        }
    },
    facet: (req, res) => {
        try {
            var query = client.createQuery()
                .q('*:*')
                .rows(1)
                .facet({
                    field: ['tag'],
                    limit: 10
                })

            client.search(query, function (err, result) {
                if (err) {
                    console.log(err);
                    return;
                }

                res.json({
                    ok: 1,
                    data: result.facet_counts
                })
            });


        } catch (err) {
            res.status(500).json({
                err: err.message
            })
        }
    }
}

module.exports = i;