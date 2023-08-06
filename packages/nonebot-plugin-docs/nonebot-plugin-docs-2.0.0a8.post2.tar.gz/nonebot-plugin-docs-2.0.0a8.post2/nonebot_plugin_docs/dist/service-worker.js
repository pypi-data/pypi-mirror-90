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
    "revision": "84f47b6809623289fde1124304b143fe"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "c41d650e289903ce93eccf093dcda261"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "72f78163e87a3e414810c3e15593b25e"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "36351c1846828de91da96a83ce8f601a"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "05011fef50be10446c5d5a4bccbace54"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "1b06fad6f4b1d2c371d78488a9380fec"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "33cb695d50bbb29c9fd51d5e75ef76a3"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "1c70b7e700fe3d7d1be9dc574f77d179"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "cf647642777c21f75c4e799978462945"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "7bd469ac3fc0683c65c8392e8b911148"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "a224555fde4f71a4a7b93527fe878008"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "9cd7857a009f35822da3a5251600e35e"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "78ef71d46eaf2d7e6276f12914dc1d27"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "64498a66b8006a9afe47ff260ac00292"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "ed2ad720d0d1cb3d2a5cfde60e4bd635"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "570efeb1410abdbb2f9155c9e3ecf589"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "feed7929062e9fbad6795bd15b7973f2"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "ac4c1e830f207ea0b2d2613470f96fa8"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "ba009164493f08d9ef6163dc042bd9ec"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "accc294409e260249ee120d73c80e97e"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "f03a53106d317e017e345c77fbdaf5e2"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "8935a4cf3f55f2be80feb3d34b354775"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "be3915bc874a1c62d9219b52dbe16082"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "7fc68e7ba3d5b7daf829b453ad88d876"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "caf1b646cf2a3f1d03b46d8fab506862"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "248064679b2a3faeeea5c875dd284bc2"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "6e5b3d1d2e057a533e686d77d3c60a8a"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "dcf78473cb13cea419f8d6fe2f1d46c5"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "9c773877ef72c99ad66ba021a6665720"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "04d68cbc96a1f2450b19208a677b4832"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "69191fcf391243fe63014f50b6be0e0a"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "8ea67631a9879fc234e5ecaa97e2bd28"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "c672d58e55891a5baf9debd0da1fffba"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "9807c4d6a03ed6de37aad3c40c1da3bb"
  },
  {
    "url": "404.html",
    "revision": "f12f79f7485b93cae963b271fca5df3e"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "fcd264ea21b2576166ab0cba28d6afbe"
  },
  {
    "url": "advanced/index.html",
    "revision": "7b0a8b17e518c6e9af505aa449c0fbea"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "af6aabec457055f49440095273c7b52a"
  },
  {
    "url": "advanced/permission.html",
    "revision": "1840c63670c138470ed99d3b1c8a2178"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "0babcb49b6d341791891c361cf7a504d"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "8f1047fdec5d157fa368f3da8160bf4c"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "ede740af22ded3c6adace87a7d57e863"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "7d8e719af8fb31c5bf3e2c9301427204"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "c6a50ad9165916fe5e9d4a9d3051fca4"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "28e79aa0c0865b0c927149fcb4e9d0c2"
  },
  {
    "url": "api/config.html",
    "revision": "298914ba9c3c85cd68c7957b13b0566e"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "d2d136c5312bb1e3c5ef53d6a64c911a"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "0cff20e196e77568eaa511dd7edc2972"
  },
  {
    "url": "api/exception.html",
    "revision": "57ea87728b926adb5c0a4d4e17ec4c70"
  },
  {
    "url": "api/index.html",
    "revision": "bea5dc20dd9f7f4dece8a233b30b3138"
  },
  {
    "url": "api/log.html",
    "revision": "8efa4cb63e7f6b4a75f035eba6bc8191"
  },
  {
    "url": "api/matcher.html",
    "revision": "98114d791e6a13483aef536a4c1afc79"
  },
  {
    "url": "api/message.html",
    "revision": "261f68f829965e5c395bd41fa1698a69"
  },
  {
    "url": "api/nonebot.html",
    "revision": "45b3cfc35fc8804fa0ba5beabef25123"
  },
  {
    "url": "api/permission.html",
    "revision": "37e5b585ebfe884ccfa2fd2304ce8f42"
  },
  {
    "url": "api/plugin.html",
    "revision": "57d31d54885f2cd6a0b0d5a163a957e2"
  },
  {
    "url": "api/rule.html",
    "revision": "9dc5e8cf39ed86a9b0e47dc465bd5b29"
  },
  {
    "url": "api/typing.html",
    "revision": "41e4b294719570a580a91e2bf9ec34e0"
  },
  {
    "url": "api/utils.html",
    "revision": "39ca0583accd6238d194de5fa7e250bd"
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
    "url": "assets/js/11.ceff5d4f.js",
    "revision": "e336ac34047f348f52a26e537097eadc"
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
    "url": "assets/js/12.d2b8531b.js",
    "revision": "669d8d107e3e5abd591a1f71cf850df7"
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
    "url": "assets/js/43.7becaf2c.js",
    "revision": "4ceafbd736de3eab7bb3b378c87349f1"
  },
  {
    "url": "assets/js/44.63dc9ae1.js",
    "revision": "1bb54d9860d247a87325e73411f1cb39"
  },
  {
    "url": "assets/js/45.ed4be8b3.js",
    "revision": "2635e600fc0a6db890f0e58a9ddda873"
  },
  {
    "url": "assets/js/46.07e6ce5e.js",
    "revision": "e093f80866882320b56a026559bbdfb3"
  },
  {
    "url": "assets/js/47.c0fb0fa9.js",
    "revision": "5163b9a41d06a04ff12133984a25dcb7"
  },
  {
    "url": "assets/js/48.2edccba4.js",
    "revision": "41b2c4f40c6e6bfd9ca5e16e09592328"
  },
  {
    "url": "assets/js/49.7a3566dd.js",
    "revision": "dd48adfb241e36a6f1fe9b5d04c966cd"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.36af2b99.js",
    "revision": "60dddb9c4a8205163b55b83e795853ad"
  },
  {
    "url": "assets/js/51.a8eed970.js",
    "revision": "4a4f2bb1d742f66c6683420b1a9d6c08"
  },
  {
    "url": "assets/js/52.159ea82f.js",
    "revision": "19ca86b4313a5eabf4d5ca98679e9335"
  },
  {
    "url": "assets/js/53.40359eaa.js",
    "revision": "735eedf5d56aac5559d209e0ce965d89"
  },
  {
    "url": "assets/js/54.c211e95e.js",
    "revision": "0ef8fae20117997cb7e8d63c73b7febf"
  },
  {
    "url": "assets/js/55.a08764e9.js",
    "revision": "b0da76cb4c1c70e9e1575c4af2f04afd"
  },
  {
    "url": "assets/js/56.058f2433.js",
    "revision": "7ead21e040a1383880275f7d5b66779e"
  },
  {
    "url": "assets/js/57.d056c155.js",
    "revision": "ea0e04dfef4b0d86e50aa9dcb8a0c139"
  },
  {
    "url": "assets/js/58.214ddb30.js",
    "revision": "bb3b799b43eb009431a23ccaef97b862"
  },
  {
    "url": "assets/js/59.e5a7cd8d.js",
    "revision": "a9ae0161ff2ca218f790b0a5507de5e5"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.87c2ecf7.js",
    "revision": "d99eddad25089fa7066bef22b969ab3d"
  },
  {
    "url": "assets/js/61.c329c250.js",
    "revision": "7d64b5e10c1da7be5c20bbf5aa2da2fd"
  },
  {
    "url": "assets/js/62.80bbfd1e.js",
    "revision": "f295d8f9775ed951a977cd2b4b04feed"
  },
  {
    "url": "assets/js/63.17c305f0.js",
    "revision": "f1b4c8b7423abf468b1dabec8817b085"
  },
  {
    "url": "assets/js/64.2292e79e.js",
    "revision": "f7ef58b5454f4ee28d76fd87af1aaf91"
  },
  {
    "url": "assets/js/65.42de834d.js",
    "revision": "ebf3b883613504591fc999ae179263eb"
  },
  {
    "url": "assets/js/66.c8347963.js",
    "revision": "f65b3b2bc689a8377cd4628bc39ddb5c"
  },
  {
    "url": "assets/js/67.91db0cd4.js",
    "revision": "5208cdc3c133fa73130facd48aaaa013"
  },
  {
    "url": "assets/js/68.1761a185.js",
    "revision": "a408ffc7f3dfe873ee92b10baabec613"
  },
  {
    "url": "assets/js/69.ceccc501.js",
    "revision": "f80a14fe0f0477642d66ec4a19d8067f"
  },
  {
    "url": "assets/js/7.28680298.js",
    "revision": "09b27a60abea1d0313f2fddec2b8600f"
  },
  {
    "url": "assets/js/70.3fd919e3.js",
    "revision": "dd3c7aa27978e7642ff8ff0c7115551b"
  },
  {
    "url": "assets/js/71.bfff2068.js",
    "revision": "d769ced27c2cd43bb1b7fad2e1b68a81"
  },
  {
    "url": "assets/js/72.127bd5c0.js",
    "revision": "436838bc9ffc124f4756a66b8801cef5"
  },
  {
    "url": "assets/js/73.39977c92.js",
    "revision": "7418331d71a4eea09be14f9e7e04144b"
  },
  {
    "url": "assets/js/74.43e12e21.js",
    "revision": "b20cc63093d4bbe2d22642c3aafa5aa2"
  },
  {
    "url": "assets/js/75.2e1f1352.js",
    "revision": "e7a69c518e36fe841bd9f9fef15b4b69"
  },
  {
    "url": "assets/js/76.8acd3704.js",
    "revision": "cf7e93a2519a8c27de0e5ce8905f595c"
  },
  {
    "url": "assets/js/77.88d6e7ac.js",
    "revision": "49f4d8b0b8c5f29eb4878983c98ca519"
  },
  {
    "url": "assets/js/78.0e3bf85a.js",
    "revision": "bbb3ddbc15590344c916846dc0293755"
  },
  {
    "url": "assets/js/79.d145f9ef.js",
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
    "url": "assets/js/app.9a470bc9.js",
    "revision": "be6daedb3abd790a48cecc78fbf21736"
  },
  {
    "url": "changelog.html",
    "revision": "630c449f8f065716279f8454f2d8401e"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "9aa133df7de88bc3f56eb2331374b6bb"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "16bb1923c532694d25f61cec2fdecbf1"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "b1a568f9840f03dd5fa13b3847dc367b"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "53c34f45003a9a0a8f0672d21c3944ee"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "6447f1abc0fecb6d0b339aa85126dbfe"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "4f26a9a68336435c955114ed4c3abb31"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "e148abd9878c9e8104a11c77411a8a2e"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "3cdc86c54db85fb7db95e1d4a0a3e2c9"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "6aa68d99ecbf877fed6584696719e9d6"
  },
  {
    "url": "guide/index.html",
    "revision": "1f8c7c11aa3c6df05e96636de184af09"
  },
  {
    "url": "guide/installation.html",
    "revision": "34fdd56c67e431b553d8bfbd78921bb1"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "562dbd736d6f8da39faeb0ac3d228f70"
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
    "revision": "b83067d00442e0b8c28eba6a208137e9"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "33ff3e0c73e4f2427aaf810e8c0b2026"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "b40b15fe42db389df54f5eb1b12eb043"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "e7d01b282a77d0a43cf79ac9598a5dea"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "6b0bcf5e44c055caf8b0daaab92952ef"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "3ad8c346788fa9228758f47aa095c20c"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "b3d4be2c09392958669e7f53507d1a22"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "f8084ebac6daa2f6df4cde5c3a95f8bf"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "1cedf3259519a44c5c8e0324aaf416d7"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "14855f264b00c2514c7660792d8fc099"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "6f598177948ec1be856fadecd74544f6"
  },
  {
    "url": "next/api/config.html",
    "revision": "2274e4076c2157309a3ea758eb6ee2ed"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "8fd2ad30409c95db95c0f99f3930dc51"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "0366a2d1edd3d6475adb0d96b606ac61"
  },
  {
    "url": "next/api/exception.html",
    "revision": "6c5bfd85a5eea58ab330f75d409784ba"
  },
  {
    "url": "next/api/index.html",
    "revision": "4110456b334516924bcef523e877d2db"
  },
  {
    "url": "next/api/log.html",
    "revision": "a3822d7e4c3e0666549dee4d795b418f"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "b406276433ec464833ece8393b7d4fd3"
  },
  {
    "url": "next/api/message.html",
    "revision": "40caa59c2ff35d30794499150d400ace"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "dd57fe6aa8371dd70e5e0c446a688a36"
  },
  {
    "url": "next/api/permission.html",
    "revision": "6a37aa7308e07e43376a28343da0c72c"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "28a9a3bc0732dd4db25aad71061b34cc"
  },
  {
    "url": "next/api/rule.html",
    "revision": "67bc9cd9724d68697bcfa543eaec1cf8"
  },
  {
    "url": "next/api/typing.html",
    "revision": "881d4c1ef21faa048b922152588592a8"
  },
  {
    "url": "next/api/utils.html",
    "revision": "2d55cb3463b5eb976102890f1a5e356d"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "fdebe6e23d26c4d2e64adf9bffaf4be1"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "3e7b181e04471194ceca86472bef6bcf"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "7d93137395b6ecc994d0f8854f45074b"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "65a4cbddfbd39178dc52280dcf20f32b"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "101245439de76f333d69809ff098e43e"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "377d8dc018677ed902eb0b78622595c3"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "6628c812f7ade8e564c1d05d9c2f0d25"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "dbaf69946aba28a0bd02366f745132e3"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "3f0389b91fad63372f5ea893b0c8ae5a"
  },
  {
    "url": "next/guide/index.html",
    "revision": "b47e13f213173a31e315f1e0413e0e52"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "75aa914caf0709237d05741257cf5f67"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "55094e9a65a2448b260e5f4c636f0068"
  },
  {
    "url": "next/index.html",
    "revision": "02b2b9a64c6bfeb4886d2212a2f131de"
  },
  {
    "url": "plugin-store.html",
    "revision": "95359eaec85e1902183f9aeacb1bcc53"
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
