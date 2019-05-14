const express = require('express');

const router = express.Router();
const app = express();

const Pages = require('../controllers/pages')

router.route('/is_alive')
    .get((req, res) => {
        res.json({
            ok: 1,
            message: "Alive"
        })
    })

router.route('/page/:page')
    .get(Pages.page)
    router.route('/facet')
    .get(Pages.facet)
    
module.exports = router;
