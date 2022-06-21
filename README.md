# Shared Vehicles APIs

## Status

| Name                | Android Package Name     | Website               | Supported |
| :------------------ | :----------------------: | :-------------------: | :-------: |
| **Acciona**         | com.acciona.mobility.app | movilidad.acciona.com |           |
| **Billy**           | bike.billy               | billy.bike            |           |
| **Bird**            | co.bird.android          | bird.co               |     X     |
| **BlueBike**        | com.motivateco.hubway    | blue-bike.be          |           |
| **Bolt**            | ee.mtakso.client         | bolt.eu               |     X     |
| **Cambio**          | de.cambio.app            | cambio.be             |           |
| **Cityscoot**       | com.livebanner.cityscoot | cityscoot.eu          |     X     |
| **Cooltra**         | com.mobime.ecooltra      | cooltra.com           |     X     |
| **Dott**            | com.ridedott.rider       | ridedott.com          |           |
| **Enjoy**           | com.eni.enjoy            | enjoy.eni.com         |           |
| **Felyx**           | com.felyx.android        | felyx.com             |     X     |
| **GoSharing**       | nl.gosharing.gourban.app | go-sharing.com        |     X     |
| **Heetch**          | com.heetch               | heetch.com |          |
| **Lime**            | com.limebike             | li.me                 |     X     |
| **NextBike**        | de.nextbike              | nextbike.de           |     X     |
| **Pony**            | co.ponybikes.mercury     | getapony.com          |     X     |
| **Poppy**           | com.gopoppy.app          | poppy.be              |     X     |
| **ShareNow**        | com.car2go               | share-now.com         |           |
| **Superpedestrian** | com.superpedestrian.link | superpedestrian.com   |     X     |
| **Swapfiet**        | com.swapfiets            | swapfiets.be          |           |
| **Tier**            | com.tier.app             | tier.app              |     X     |
| **Veligo**          | com.idfmobilites.veligo  | veligo-location.fr    |           |
| **Villo**           | com.altairapps.villo     | villo.be              |     X     |
| **Voi**             | io.voiapp.voi            | voiscooters.com       |     X     |
| **Yego**            | com.getyugo.app          | rideyego.com          |           |
| **ZigZag**          | it.zero11.app.zigzag     | zigzagsharing.com     |           |
| **Zoov**            | io.birota.zoov           | zoov.eu               |           |

---

## Get vehicles list from API

| Name                |                              Endpoint                             |  Token Type   |           Token Infos           |
| :------------------ | :---------------------------------------------------------------: | :-----------: | :-----------------------------: |
| **Acciona**         |                                 ?                                 |       ?       |                ?                |
| **Billy**           |                                 ?                                 |       ?       |                ?                |
| **Bird**            | api-bird.prod.birdapp.com/bird/nearby                             | Dynamic Token | Bearer, 1050 ascii characters   |
| **BlueBike**        |                                 ?                                 |       ?       |                ?                |
| **Bolt**            | node.bolt.eu/rental-search/categoriesOverview                     | Account Token | Base64, phone number + 16 bytes |
| **Cambio**          |                                 ?                                 |       ?       |                ?                |
| **Cityscoot**       | cityscoot.eu/api/scooters/public/city/                            | Device Token  | 8 bytes                         |
| **Cooltra**         | api.zeus.cooltra.com/mobile_cooltra/v1/vehicles                   | App Token     | Bearer, 32 bytes                |
| **Dott**            |                                 ?                                 |       ?       |                ?                |
| **Enjoy**           |                                 ?                                 |       ?       |                ?                |
| **Felyx**           | relay.felyx.com/map/cars                                          | No Token      |                                 |
| **GoSharing**       | platform.api.gourban.services/v1/greenmo/front/vehicles           | No Token      |                                 |
| **Heetch**          |                                 ?                                 |       ?       |                ?                |
| **Lime**            | web-production.lime.bike/api/rider/v1/views/map                   | Account Token | Bearer, 127 ascii characters    |
| **NextBike**        | maps.nextbike.net/maps/nextbike-live.flatjson                     | App Token     | 16 alphanum characters          |
| **Pony**            | wss://pony-bikes-f8cf9.firebaseio.com/.ws?ns=pony-bikes-f8cf9&v=5 | No Token      |                                 |
| **Poppy**           | poppy.red/api/v2/vehicles                                         | No Token      |                                 |
| **ShareNow**        |                                 ?                                 |       ?       |                ?                |
| **Superpedestrian** | vehicles.linkyour.city/reservation-api/local-vehicles/            | Device Token  | 16 bytes                        |
| **Swapfiet**        |                                 ?                                 |       ?       |                ?                |
| **Tier**            | platform.tier-services.io/v2/vehicle                              | App Token     | 24 alphanum characters          |
| **Veligo**          |                                 ?                                 |       ?       |                ?                |
| **Villo**           | api.jcdecaux.com/vls/v3/stations                                  | App Token     | 20 bytes                        |
| **Voi**             | api.voiapp.io/v2/rides/vehicles                                   | Dynamic Token | 639 ascii characters            |
| **Yego**            |                                 ?                                 |       ?       |                ?                |
| **ZigZag**          |                                 ?                                 |       ?       |                ?                |
| **Zoov**            |                                 ?                                 |       ?       |                ?                |