# Shared Vehicles APIs

## Status

| Name                | Android Package Name     | Supported |
| :------------------ | :----------------------: | :-------: |
| **Acciona**         | com.acciona.mobility.app |           |
| **Billy**           | bike.billy               |           |
| **Bird**            | co.bird.android          |     X     |
| **BlueBike**        | com.motivateco.hubway    |           |
| **Bolt**            | ee.mtakso.client         |     X     |
| **Cambio**          | de.cambio.app            |           |
| **Cityscoot**       | com.livebanner.cityscoot |     X     |
| **Cooltra**         | com.mobime.ecooltra      |     X     |
| **Dott**            | com.ridedott.rider       |           |
| **Enjoy**           | com.eni.enjoy            |           |
| **Felyx**           | com.felyx.android        |     X     |
| **GoSharing**       | nl.gosharing.gourban.app |     X     |
| **Heetch**          | com.heetch               |           |
| **Lime**            | com.limebike             |     X     |
| **NextBike**        | de.nextbike              |     X     |
| **Pony**            | co.ponybikes.mercury     |     X     |
| **Poppy**           | com.gopoppy.app          |     X     |
| **ShareNow**        | com.car2go               |           |
| **Superpedestrian** | com.superpedestrian.link |     X     |
| **Swapfiet**        | com.swapfiets            |           |
| **Tier**            | com.tier.app             |     X     |
| **Veligo**          | com.idfmobilites.veligo  |           |
| **Villo**           | com.altairapps.villo     |     X     |
| **Voi**             | io.voiapp.voi            |     X     |
| **Yego**            | com.getyugo.app          |           |
| **ZigZag**          | it.zero11.app.zigzag     |           |
| **Zoov**            | io.birota.zoov           |           |

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