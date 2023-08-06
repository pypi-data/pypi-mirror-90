/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "9a5f8275fb82bf86a5ffcdc5d0ee52a0"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "bae67dff150f9bfb1a5d3154e567d3c9"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "d613088cb0f853ddf986dddb0c035c38"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "0ef5848869284724108c3dd3c76c3de9"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "f91bf09349ede356cfe2420e036ab2cd"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "fddd4c60047584d8179bf44b47f3914b"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "1c1ecb061eae03c0b34d3ac60a0cc27c"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "254720f7cb53e4bec625604f877aaa34"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "16f7ab1355edf69386efe8143c403865"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "06dccf1f9e05d1310d56763106ea4c2e"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "f1b2ac6867116b616de6ac7a3d51eaed"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "ef81001cfad086e70269ac33126e17b6"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "7f24a190f05a1f17d1ffe45ae7fa87dd"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "8fedad3981897bc1c5ba8e2907206317"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "1113e53cda48f3cb9082da7fb95184b6"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "67eee967e78b416f8d20ab214bc89c35"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "3431f459aa4e70981a269c855cf91c09"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "c1b8a9358388d9137c6fcce6cb0c9bea"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "db1c35ad78a24d12710aac9ec24b6dab"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "ac79c0a3901549d211d3aa70c861ec5d"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "327325502e3f7476920af7a794ecde61"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "37ed71bd2b8853c650f9babc6793d9fc"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "f4f76a6b041a4c8f9f131f484372614a"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "06aff13a9e5ecba4dda6543f6e86cf4e"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "290a93052d2e1629cf48fe8c4e57ecad"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "db954dbf8f7014d34e2e450ce285a651"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "ea5995fed583675ac44c64affd6974a4"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "9b03b69d5a2af896aca341067d3b9f1d"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "913ef95f756939114eab2d4a40032ef5"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "a73fc7670834de3a65ebf4f62845082a"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "6b54b7932c9d41d17e68f453a79c23f1"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "9ed8b5dc385941da7884785074913155"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "9b0c9a4f1066758ca2d32edf4f614ed2"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "275efbaa5b7b8d199376191e9f0c68a9"
  },
  {
    "url": "404.html",
    "revision": "99980fb18ab4b371969f171027cb5084"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "b6963ac4c2cb31bf6ec04338d4506eb1"
  },
  {
    "url": "advanced/index.html",
    "revision": "398f2cca197859ffca2dd59a0bed1d65"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "fd9da7336402540ae8031fcabf19f6c6"
  },
  {
    "url": "advanced/permission.html",
    "revision": "9c16a317419b464964c296f175e75c10"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "4f508a2b4b0a6727a61d1ef32092fa79"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "ba726a97a3ed965c41c98a570befcbb8"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "69e958c08e5486b782162d0ee60cad38"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "677b4cc03e1cd62938088b3bf018e714"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "d49ed34a0ee25fba327f0a806aa78af7"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "1c9972ffc8206414dbaae69910a56406"
  },
  {
    "url": "api/config.html",
    "revision": "07b40a9d5b8f302660828fbd855fe873"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "d8142d6b876c8607aad42dcc7a0388dc"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "8ff562672268da4cdefa5bc5f0f2b08e"
  },
  {
    "url": "api/exception.html",
    "revision": "e8a9fe5730a0f5bfaf17721fc17bbe90"
  },
  {
    "url": "api/index.html",
    "revision": "0ddefb479dc4d6a939b5e862a8889832"
  },
  {
    "url": "api/log.html",
    "revision": "f408e791f5bc9ccd794b43252ad5664a"
  },
  {
    "url": "api/matcher.html",
    "revision": "b19d4124fe612ed8244866c4dd43a883"
  },
  {
    "url": "api/message.html",
    "revision": "b3f4006d10a7e49d8ceca51f10c7d90e"
  },
  {
    "url": "api/nonebot.html",
    "revision": "2987b9f46ca81cec936ee99d3164ddb9"
  },
  {
    "url": "api/permission.html",
    "revision": "668c9b072605a2db5743e8c711dab9da"
  },
  {
    "url": "api/plugin.html",
    "revision": "fa284f9ac0c27a6a94cd71abf06a257d"
  },
  {
    "url": "api/rule.html",
    "revision": "d890f1a7476ba5978e14e0a3e6310f72"
  },
  {
    "url": "api/typing.html",
    "revision": "aa898ba381dece58248c6ce5bbde067c"
  },
  {
    "url": "api/utils.html",
    "revision": "766801c7fc842caee9722f33c4d44650"
  },
  {
    "url": "assets/css/0.styles.49c81ce6.css",
    "revision": "16daa387e964eb70cfc34b4c8cbabd5c"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.28c1c8c5.js",
    "revision": "840072ff191b8b2516fba79dbe6b8236"
  },
  {
    "url": "assets/js/100.0aa2b9c9.js",
    "revision": "778a20b83d857a906fd00a55045ab1c7"
  },
  {
    "url": "assets/js/101.ba344a23.js",
    "revision": "d6103d86dc75a6842df06cb97908b677"
  },
  {
    "url": "assets/js/102.108a3ef7.js",
    "revision": "9a1c40c0b821a6afe1ea15aeee554504"
  },
  {
    "url": "assets/js/103.faeaccd7.js",
    "revision": "42f473780a990d12b59c356c28c171d3"
  },
  {
    "url": "assets/js/104.e855e28f.js",
    "revision": "0fb7bc0d02e127656807a0f5df6d3106"
  },
  {
    "url": "assets/js/105.5fa4f2d5.js",
    "revision": "15b40638687ba9b0bad1be66e04fb1a9"
  },
  {
    "url": "assets/js/106.e2d52cf9.js",
    "revision": "fd574600e4d39419f8befcc78f386ec6"
  },
  {
    "url": "assets/js/107.53a79303.js",
    "revision": "089253c390fb1540591a92013fd91473"
  },
  {
    "url": "assets/js/108.7d4e281c.js",
    "revision": "5e7fd220549e0583759052b30afac2f2"
  },
  {
    "url": "assets/js/109.97b76e28.js",
    "revision": "812988139e51bfef08b81412b7e57781"
  },
  {
    "url": "assets/js/11.23246db0.js",
    "revision": "9b74e75eea9ae2049a02db798d08f26d"
  },
  {
    "url": "assets/js/110.55ae0f89.js",
    "revision": "6e039eb152499f29ea27dcd8274a7e84"
  },
  {
    "url": "assets/js/111.71469f9f.js",
    "revision": "b1f7f85bfd92c2ec3c8188aab61ba3d0"
  },
  {
    "url": "assets/js/112.e36b2662.js",
    "revision": "850d258e87a02c633ec03e6570a6a7bd"
  },
  {
    "url": "assets/js/113.494cefad.js",
    "revision": "4bc5b14c6a4bf456cd7115a30c65ad04"
  },
  {
    "url": "assets/js/114.84070937.js",
    "revision": "23bbf0b8fd74e9d547f211ce028d3601"
  },
  {
    "url": "assets/js/115.b33db9e9.js",
    "revision": "5bd4990f3a25d6bc18c60b59c50e4662"
  },
  {
    "url": "assets/js/116.836b6017.js",
    "revision": "e9710379090aef2cf126da09312978e3"
  },
  {
    "url": "assets/js/117.1f3fd674.js",
    "revision": "8baeb7bb80fe3e3f5dc00a9017d405b8"
  },
  {
    "url": "assets/js/118.91f9645f.js",
    "revision": "ffb9d0b715dfc81f0979b066d85a0a01"
  },
  {
    "url": "assets/js/119.34ffba23.js",
    "revision": "fda062dd2a4773c9231a17097733d76c"
  },
  {
    "url": "assets/js/12.272c6820.js",
    "revision": "a71b251392e4ae8f1fe2813ecceb8b88"
  },
  {
    "url": "assets/js/13.b09abc6d.js",
    "revision": "2a7894cf81be8f243955471dcc6222a4"
  },
  {
    "url": "assets/js/14.3b7d1b68.js",
    "revision": "659ea06188f0514d9fbadb894f3db694"
  },
  {
    "url": "assets/js/15.bf0eddf5.js",
    "revision": "df99b1d3019b1d7cfe0be338dc00a2c1"
  },
  {
    "url": "assets/js/16.2585a0f8.js",
    "revision": "786660c791530788b6978145c5156ab2"
  },
  {
    "url": "assets/js/17.49ba0f55.js",
    "revision": "2e2599c13a2cb684dc114610f1c13a6b"
  },
  {
    "url": "assets/js/18.c8dd93fb.js",
    "revision": "de183ac0a3a7a37a71b1b6e9af29c4c4"
  },
  {
    "url": "assets/js/19.85f95c64.js",
    "revision": "5ee20fb4e85b8e4bf0c741c6138b61d8"
  },
  {
    "url": "assets/js/2.c84f7eb9.js",
    "revision": "69bb4fc50d5d4831886aa38cb858ad97"
  },
  {
    "url": "assets/js/20.7e10e37d.js",
    "revision": "85245eeca1bca187ee381f7cac6b903b"
  },
  {
    "url": "assets/js/21.45cb5d06.js",
    "revision": "1711246a7f6b6cd6f18f7e6830fd2954"
  },
  {
    "url": "assets/js/22.303d9965.js",
    "revision": "56a8a768c72d50ca8e4407c479913897"
  },
  {
    "url": "assets/js/23.8481bf65.js",
    "revision": "ed5d88719c298b86db622b27a5b2e14e"
  },
  {
    "url": "assets/js/24.ebd72834.js",
    "revision": "43b49c55a78bfd9fd972ff27290c60bc"
  },
  {
    "url": "assets/js/25.0682441d.js",
    "revision": "fec7aa55a02fdcd8b7367844fa8a9717"
  },
  {
    "url": "assets/js/26.92eb06d9.js",
    "revision": "04a9df6c7482d7e6235b49c743856f80"
  },
  {
    "url": "assets/js/27.01082146.js",
    "revision": "d97b94453de98ce30b5f130aa85f6b8e"
  },
  {
    "url": "assets/js/28.e960975c.js",
    "revision": "c3227657205b50d251673a090b3c1834"
  },
  {
    "url": "assets/js/29.7a94e670.js",
    "revision": "955ea3daf7f28509e0513e80b19242bc"
  },
  {
    "url": "assets/js/3.87435b6a.js",
    "revision": "4d71ee736540cb05cb380b36643921cc"
  },
  {
    "url": "assets/js/30.486615ee.js",
    "revision": "37c305207221b9d52ce4e2c5617f78ed"
  },
  {
    "url": "assets/js/31.c319ab9f.js",
    "revision": "1002edff36bda4e5657e521f56eff936"
  },
  {
    "url": "assets/js/32.a9811cfc.js",
    "revision": "07fe2195d50b27d499aecaa890c89f6e"
  },
  {
    "url": "assets/js/33.7bb3c874.js",
    "revision": "d0b5f97695a1849aa16818696778d650"
  },
  {
    "url": "assets/js/34.27202e66.js",
    "revision": "1040016006e3ff67819660abba666ed7"
  },
  {
    "url": "assets/js/35.7f2205ba.js",
    "revision": "cfabea12a7c0d3c6d56c336d8774ad40"
  },
  {
    "url": "assets/js/36.990546b5.js",
    "revision": "d68def4aae99716f5e2580235e5bac52"
  },
  {
    "url": "assets/js/37.b45f9312.js",
    "revision": "3c33dccd3ed1e5533eae2bb080653e84"
  },
  {
    "url": "assets/js/38.b054f867.js",
    "revision": "0e365b1a606052dae0d73e77385d38ed"
  },
  {
    "url": "assets/js/39.eae4a822.js",
    "revision": "0d0dfca03c6bc4638d1cfd0fa3119a85"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.2e55c49a.js",
    "revision": "914bca3ba4a91eb9f74f313043f0badf"
  },
  {
    "url": "assets/js/41.dcc2aabb.js",
    "revision": "df400969eeaea2c3114f8705b19c367a"
  },
  {
    "url": "assets/js/42.e1536973.js",
    "revision": "1ef9ca425234140a05af1998bf39393c"
  },
  {
    "url": "assets/js/43.915c5488.js",
    "revision": "4ceafbd736de3eab7bb3b378c87349f1"
  },
  {
    "url": "assets/js/44.fbbab372.js",
    "revision": "1bb54d9860d247a87325e73411f1cb39"
  },
  {
    "url": "assets/js/45.b66e0857.js",
    "revision": "2635e600fc0a6db890f0e58a9ddda873"
  },
  {
    "url": "assets/js/46.54ce656e.js",
    "revision": "e093f80866882320b56a026559bbdfb3"
  },
  {
    "url": "assets/js/47.9871143d.js",
    "revision": "5163b9a41d06a04ff12133984a25dcb7"
  },
  {
    "url": "assets/js/48.228f65ec.js",
    "revision": "41b2c4f40c6e6bfd9ca5e16e09592328"
  },
  {
    "url": "assets/js/49.ec6ad4e6.js",
    "revision": "dd48adfb241e36a6f1fe9b5d04c966cd"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.2b6d4b31.js",
    "revision": "60dddb9c4a8205163b55b83e795853ad"
  },
  {
    "url": "assets/js/51.0804466b.js",
    "revision": "4a4f2bb1d742f66c6683420b1a9d6c08"
  },
  {
    "url": "assets/js/52.19bfea4b.js",
    "revision": "19ca86b4313a5eabf4d5ca98679e9335"
  },
  {
    "url": "assets/js/53.f69fcdc6.js",
    "revision": "735eedf5d56aac5559d209e0ce965d89"
  },
  {
    "url": "assets/js/54.02bdf591.js",
    "revision": "0ef8fae20117997cb7e8d63c73b7febf"
  },
  {
    "url": "assets/js/55.4aabf789.js",
    "revision": "b0da76cb4c1c70e9e1575c4af2f04afd"
  },
  {
    "url": "assets/js/56.156c36a0.js",
    "revision": "7ead21e040a1383880275f7d5b66779e"
  },
  {
    "url": "assets/js/57.4608dc2b.js",
    "revision": "ea0e04dfef4b0d86e50aa9dcb8a0c139"
  },
  {
    "url": "assets/js/58.24533b60.js",
    "revision": "bb3b799b43eb009431a23ccaef97b862"
  },
  {
    "url": "assets/js/59.2615189b.js",
    "revision": "a9ae0161ff2ca218f790b0a5507de5e5"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.9487556b.js",
    "revision": "d99eddad25089fa7066bef22b969ab3d"
  },
  {
    "url": "assets/js/61.af465937.js",
    "revision": "7d64b5e10c1da7be5c20bbf5aa2da2fd"
  },
  {
    "url": "assets/js/62.42ab8c00.js",
    "revision": "f295d8f9775ed951a977cd2b4b04feed"
  },
  {
    "url": "assets/js/63.b1adb08a.js",
    "revision": "f1b4c8b7423abf468b1dabec8817b085"
  },
  {
    "url": "assets/js/64.c249a973.js",
    "revision": "f7ef58b5454f4ee28d76fd87af1aaf91"
  },
  {
    "url": "assets/js/65.15941700.js",
    "revision": "ebf3b883613504591fc999ae179263eb"
  },
  {
    "url": "assets/js/66.980bc97a.js",
    "revision": "f65b3b2bc689a8377cd4628bc39ddb5c"
  },
  {
    "url": "assets/js/67.3f2653d4.js",
    "revision": "5208cdc3c133fa73130facd48aaaa013"
  },
  {
    "url": "assets/js/68.484eeaca.js",
    "revision": "a408ffc7f3dfe873ee92b10baabec613"
  },
  {
    "url": "assets/js/69.f6f36a0e.js",
    "revision": "f80a14fe0f0477642d66ec4a19d8067f"
  },
  {
    "url": "assets/js/7.28680298.js",
    "revision": "09b27a60abea1d0313f2fddec2b8600f"
  },
  {
    "url": "assets/js/70.b662505c.js",
    "revision": "dd3c7aa27978e7642ff8ff0c7115551b"
  },
  {
    "url": "assets/js/71.a994ac49.js",
    "revision": "d769ced27c2cd43bb1b7fad2e1b68a81"
  },
  {
    "url": "assets/js/72.b534cfe6.js",
    "revision": "436838bc9ffc124f4756a66b8801cef5"
  },
  {
    "url": "assets/js/73.86170eaa.js",
    "revision": "7418331d71a4eea09be14f9e7e04144b"
  },
  {
    "url": "assets/js/74.bd705444.js",
    "revision": "b20cc63093d4bbe2d22642c3aafa5aa2"
  },
  {
    "url": "assets/js/75.2e85bb30.js",
    "revision": "e7a69c518e36fe841bd9f9fef15b4b69"
  },
  {
    "url": "assets/js/76.056ee8eb.js",
    "revision": "cf7e93a2519a8c27de0e5ce8905f595c"
  },
  {
    "url": "assets/js/77.f78a4b1f.js",
    "revision": "49f4d8b0b8c5f29eb4878983c98ca519"
  },
  {
    "url": "assets/js/78.b30bbccb.js",
    "revision": "bbb3ddbc15590344c916846dc0293755"
  },
  {
    "url": "assets/js/79.965fdb62.js",
    "revision": "96e2039e286f7ed82f612cb2682012cf"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.fff6a2fd.js",
    "revision": "76cfa742ed08498cb6be80f246c394f3"
  },
  {
    "url": "assets/js/81.c673fcb9.js",
    "revision": "ad427706a86f6ec44ba45a766cd5452f"
  },
  {
    "url": "assets/js/82.abce9fae.js",
    "revision": "57c707c7929d518fdf241387a6f3d232"
  },
  {
    "url": "assets/js/83.bdb2a65e.js",
    "revision": "44afd6d62ce7b6ddba10a2f7ecbd0a0d"
  },
  {
    "url": "assets/js/84.2ba31590.js",
    "revision": "a097e4ac49151db551ac4c1a67c68136"
  },
  {
    "url": "assets/js/85.ce4858f3.js",
    "revision": "c7419b7a8ae79f081333b05fb22a3f5b"
  },
  {
    "url": "assets/js/86.0cfe6d73.js",
    "revision": "fedb1ce310203b5cf7e85a49e7268b0b"
  },
  {
    "url": "assets/js/87.3a3966aa.js",
    "revision": "d99e32ea44df925efaeb5e38397224b2"
  },
  {
    "url": "assets/js/88.7df4f597.js",
    "revision": "1c9a25d0e98c07ea69aa9488da8e0924"
  },
  {
    "url": "assets/js/89.9b3bdeee.js",
    "revision": "7e9ac126d2d2604cd3ecee13a94becb4"
  },
  {
    "url": "assets/js/9.a3422899.js",
    "revision": "1778058aa634fb91f13f373b79370972"
  },
  {
    "url": "assets/js/90.e9d0f1f1.js",
    "revision": "4b870bc29d4649c7353b7b432316c13d"
  },
  {
    "url": "assets/js/91.f7f5aa29.js",
    "revision": "7fb1d579881368e2a596e0c0d55b7c8b"
  },
  {
    "url": "assets/js/92.bdb0b593.js",
    "revision": "be2a1a9cc09f01fef1e84748d126dec9"
  },
  {
    "url": "assets/js/93.31d223c1.js",
    "revision": "d286ec418c7d545fea29e6882c7c6863"
  },
  {
    "url": "assets/js/94.6f75de56.js",
    "revision": "00ede32cd6142a1196f9c2ca2320a30b"
  },
  {
    "url": "assets/js/95.3635ce13.js",
    "revision": "d097c8b6be2314c94dc2d107009a0fa8"
  },
  {
    "url": "assets/js/96.5355fdcd.js",
    "revision": "51b0ba8787c43f04e2d9fa7d49a26acd"
  },
  {
    "url": "assets/js/97.ac7f21fa.js",
    "revision": "9a75f711369a357e850a8de97e3a3cc3"
  },
  {
    "url": "assets/js/98.567d92ad.js",
    "revision": "5fcf89db1ef7525fe66e31a36f10b84b"
  },
  {
    "url": "assets/js/99.9cc2aeff.js",
    "revision": "47cade6d8543a23238b42e0e165a926b"
  },
  {
    "url": "assets/js/app.cf93dabc.js",
    "revision": "9223709a7250abcfc1a7f5de06e50b5b"
  },
  {
    "url": "changelog.html",
    "revision": "e2e7785e3e6fcd6499b3264444914109"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "3d168a8ecf49573d78f3762924eeeb1d"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "8ed989f3c1c301f883b99d55c1c64c4a"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "a113d42ce5c5028476c9359c18167bf4"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "28b06a362e3ca735ec55f24fff571bc1"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "326c5998ac534ab15936cc9812cd2613"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "84ae268559a47ced0b4c590e7d9f2904"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "8fad651ac8b5f6ed537c038d9ac60ade"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "a4df29b0f06c4ac494b2f84acd766ff3"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "058d74d8615e76a88909e66df32e60df"
  },
  {
    "url": "guide/index.html",
    "revision": "b00d6bb0df7a411acb16a67923352401"
  },
  {
    "url": "guide/installation.html",
    "revision": "0ccb4ec24acbcf63d36936e1b12131b3"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "d5b2168b86295929acf6198229657c70"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "c471b970d7cb96126bdd611ae4836a42"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "1551018423fa9663015ecee8631c9596"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "ef53d74e2c315405f97210a800b6afff"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "3b23d2334e3b35de47d3edace07c2247"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "ddc9f1ab5f84354dac03c4ddaed24a97"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "ecf076da35da5a93df105ee390e2db09"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "6d5d8e0ee6707c39238dbd616abcfeef"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "95d2101a6d804aa6a20d2559b19fd4d4"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "e616c86b228261e1a1afc521172d0d14"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "42388ab52eeb07c6026d32466ba337db"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "8255f5deedd5813bced97991cfacb552"
  },
  {
    "url": "next/api/config.html",
    "revision": "c9f40b893f712d8dad6582f91a3d72dc"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "3f9bd6e957b34f20599208670455fc79"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "6cd58a3a107d4c01af1e5f9e176404a0"
  },
  {
    "url": "next/api/exception.html",
    "revision": "3e42d9aeaf384d8e5c78844abc7a5580"
  },
  {
    "url": "next/api/index.html",
    "revision": "a1e1e6bc7c7162d450aae40f10af5c3a"
  },
  {
    "url": "next/api/log.html",
    "revision": "9ff5e6fe87f32c5f81b608ad77a0ec1d"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "602d3e69d61e18362efab0aa4c594b4f"
  },
  {
    "url": "next/api/message.html",
    "revision": "256aacdc9127fa9b62785d6e3a7fa08c"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "791191b289f29b5c1bb2cd80fc8ee977"
  },
  {
    "url": "next/api/permission.html",
    "revision": "2a447cfdd999ef77e5b1b9fb9c0f0e12"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "101a329da0690411f4386c7b67e8d043"
  },
  {
    "url": "next/api/rule.html",
    "revision": "326bb9025d11a2ed37a3112f3fe428fe"
  },
  {
    "url": "next/api/typing.html",
    "revision": "3d6002bcda12b8b40c99857c91516d6d"
  },
  {
    "url": "next/api/utils.html",
    "revision": "694550fb3b6aa7d8d950ba2587d94404"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "82269fb1ae9816c6f1569fd1359f55eb"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "2fc2c56645ec9f1e75163bd9b68af3bd"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "debd96aec74e668991988d63afa03486"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "e977eb483ff368a07bf996da084cbded"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "3125124401864807f31d27abe417cb6b"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "f748cd0ae9782d63bf3786be204a8df8"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "c163704f3cd7d8a058dadb510e421821"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "5b6b5b312661033a32921ed1a453483d"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "ff94b071070262b4be7a887ab9099130"
  },
  {
    "url": "next/guide/index.html",
    "revision": "6f0e95bad4353ed4dc981a95c591351d"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "95b6362b76e46ce07363b7ccf46d0736"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "3fbbb8b0e9583a482d3a7c44dbaae939"
  },
  {
    "url": "next/index.html",
    "revision": "0c66bcbc0c4baa86742dee3655ff52d0"
  },
  {
    "url": "plugin-store.html",
    "revision": "8967b0123cd874c1bcb323534f2f3358"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
