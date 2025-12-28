#!/usr/bin/env python3
"""
Script to add the new messenger data with channel/group structure
"""

import json
import os
from datetime import datetime
from cleanup_unknown_timestamps import cleanup_data_structure

MESSENGER_FILE = 'messenger_groups.json'

# Your new data
new_data = {
    "Title": "Bangladesh Awami League",
    "Sub_Title": "Channel\n  · 53.2K members",
    "source": "https://www.messenger.com/t/9326713427339811",
    "author_url": "https://www.facebook.com/profile.php?id=166064673583399",
    "author_id": "166064673583399",
    "icon": "https://scontent.fdac31-1.fna.fbcdn.net/v/t1.15752-9/462581636_1502069793810508_6755015222113481180_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=102&ccb=1-7&_nc_sid=089eef&_nc_ohc=G7d2dKHMU1EQ7kNvwGGSl4G&_nc_oc=AdnmGsYTcFGKVEE8HsPtInwOecjNWDyTD7jgomI46YPrfClbpqr9yagDEbs9kZjaiEI&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-1.fna&oh=03_Q7cD4AFIoF-X4-9APaOhx66ndIDkLau0lNc-n280xQc7bI0wOw&oe=696F465B",
    "messages": [
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/v/17nkCnigC4/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0"
            ],
            "timestamp": "2025-12-21 22:09:00",
            "reactions": {
                "👍": 69,
                "❤": 23,
                "😢": 6
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/p/1G7H5coVtL/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-6/599962080_1341233474699598_3363166709192536966_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=103&ccb=1-7&_nc_sid=127cfc&_nc_ohc=urP93LXTEgUQ7kNvwFvHsoO&_nc_oc=AdlsZaAl9kqNiU4s8ZXUg2QC77IcLR1KxP70o5PxtUhXYuGkEK6GEppBU2VgWQEhNTw&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AfnUgOc795UXsGU4-t28PKdBpxYhrjZhn7AaBfyHeIrvfg&oe=694DA71C"
            ],
            "timestamp": "2025-12-21 04:59:00",
            "reactions": {
                "❤": 167,
                "👍": 58,
                "😢": 39
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-6/600379414_1341196584703287_5856932108534534206_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=108&ccb=1-7&_nc_sid=833d8c&_nc_ohc=poIKE0XlD7sQ7kNvwHVEZ7c&_nc_oc=AdljY790-87jCj_vX88ziXzP1FW1QUyenT2sycGQh_EevEjynUvHkqBm-eojdjSuWEE&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AfkBIhK5QG0Gwq112Pf0-F0rCy7G2gFKd0zrZb9-_0LmVA&oe=694DB473"
            ],
            "timestamp": "2025-12-21 03:54:00",
            "reactions": {
                "🖤": 104,
                "👍": 68,
                "❤": 48
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/v/1BGjwxK1cU/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t15.5256-10/596756049_1906165046649119_5112234041344848545_n.jpg?stp=dst-jpg_p261x260_tt6&_nc_cat=1&ccb=1-7&_nc_sid=032300&_nc_ohc=Cj7vWBMCHmIQ7kNvwETVO0D&_nc_oc=AdmTue8psUEmMBcSIEgf4qO-GIrHdedGucwg9cBy0U6FpIpnri1eGXYB-4EcpLcf_Nk&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_Afk-T_zLE9a8KtqwdDj1nuTQCoJGQm4MhpaDv5NUdDFYpQ&oe=694DAD54"
            ],
            "timestamp": "2025-12-21 02:43:00",
            "reactions": {
                "❤": 125,
                "👍": 42,
                "😆": 5
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t15.5256-10/602413882_844897701496341_7976661380162489542_n.jpg?stp=dst-jpg_p261x260_tt6&_nc_cat=101&ccb=1-7&_nc_sid=032300&_nc_ohc=mBci0GfImZYQ7kNvwHaJDei&_nc_oc=AdkATaL62hEZIKMIsYo31UDHrP4md4DnHR3m-qiQb3R9uForsofJgdK-qEqOOJPhHqI&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_Afk9IwTVjwaijf_v3W6Z9YZhKwYwIMii2GCvTBHUvn0hFA&oe=694DB511"
            ],
            "timestamp": "2025-12-21 01:35:00",
            "reactions": {
                "❤": 129,
                "👍": 42,
                "😢": 18
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/p/17uqfpZWbi/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-6/598535702_1340908778065401_8306022898995966005_n.jpg?stp=dst-jpg_p480x480_tt6&_nc_cat=104&ccb=1-7&_nc_sid=127cfc&_nc_ohc=jAVtAjkySj0Q7kNvwFl_6Oc&_nc_oc=AdkJpGc706kutJjiO0PQJP-GgN_ovSdfYExgT7NuSvLRCRIupz5pgqGPxLOp998Z5rs&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AfnY3QnUYNxGnl5sIC8tAvixA27M9GtWHp7MAMS2FxtCcg&oe=694DA56C"
            ],
            "timestamp": "2025-12-20 22:00:00",
            "reactions": {
                "❤": 176,
                "👍": 58,
                "🥰": 17
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/p/1FV73URJAs/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-6/600886716_1340435158112763_2232907479853010215_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=104&ccb=1-7&_nc_sid=127cfc&_nc_ohc=0yL86eeti1YQ7kNvwGOK_D6&_nc_oc=AdkJLFxqP2yNfrlqcMwGNW-SGwDGxBoWPEeZP6LCtBFP1TuajtYcARhkGdLv5sUXG8I&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_Afn27HYe53kGttYeNBk5hPI0HVVcklmned2oOSrhbkEPXQ&oe=694DA1D0"
            ],
            "timestamp": "2025-12-20 11:40:00",
            "reactions": {
                "❤": 187,
                "👍": 59,
                "😢": 37
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/p/1AXK7Wu3Ry/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-6/600291004_1340435751446037_8169434784336116934_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=100&ccb=1-7&_nc_sid=127cfc&_nc_ohc=CPcSEg4E2c0Q7kNvwGWKl7U&_nc_oc=AdnoZKLB72FaQQ40GwS_o2lLklL38YnMFw_uNzTjrCIO6BSIafJAV__-nK5-HtGJDa4&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflwsOaWZv_PF0PpRfChjnWQuOkrxgGM26s3oJbVfSXLgw&oe=694DAF62"
            ],
            "timestamp": "2025-12-20 10:47:00",
            "reactions": {
                "👍": 127,
                "❤": 60,
                "💘": 13
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/v/1EtvXziYQ3/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-1.fna.fbcdn.net/v/t15.5256-10/602391492_1124954136218771_141822298575020326_n.jpg?stp=dst-jpg_p261x260_tt6&_nc_cat=109&ccb=1-7&_nc_sid=032300&_nc_ohc=VMLxWnWnA-EQ7kNvwEvjslv&_nc_oc=AdlAMy7vpJf6bkgrV8-eAVmSmhKOSRoHCBEooSuv3zUOH-5iFWHLYzvA2DJyS0miuMQ&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fdac31-1.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AfmZ9CSg1hpNRbEHMvJJxRdrfPLOk9HhBON0hQGewsEa6w&oe=694DB5BB"
            ],
            "timestamp": "2025-12-20 04:15:00",
            "reactions": {
                "❤": 189,
                "👍": 61,
                "😢": 25
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "ইউনুস আর জামাতের উন্মত্ত মবের তান্ডব দেখলো বাংলাদেশ\n https://www.facebook.com/share/r/1CaV1eP3cf/?mibextid=wwXIfr",
            "media": [
                "https://static.xx.fbcdn.net/images/emoji.php/v9/t1f/2/16/27a1.png",
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0"
            ],
            "timestamp": "2025-12-19 20:03:00",
            "reactions": {
                "😢": 215,
                "❤": 58,
                "😡": 16
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/v/1Buwfy1dxK/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0"
            ],
            "timestamp": "2025-12-19 05:27:00",
            "reactions": {
                "👍": 174,
                "❤": 65,
                "😢": 21
            }
        },
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=11a88f&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=SlsMC91n_nOfS3v-y8SJNQ&oh=00_AfnBOyzVBpniaXSpzAulTEJoKbLEi8bZMndO-ZmeSNWuIA&oe=694DADA0",
            "text": "https://www.facebook.com/share/v/1DHVxzTR6s/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=1&ccb=1-7&_nc_sid=982592&_nc_ohc=BArLEKPiXTwQ7kNvwFrA4Q1&_nc_oc=AdmIeXzuUKR-BVRbD0Y6fxx2bSxa7hlfcEZ8ZDP5gXLl2_jVwdSXJU8ZHQQcBR5stO0&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent.fdac31-2.fna&_nc_gid=LLx62ScRjmLHsRgZ6vo7bA&oh=00_AflmqO_F1k6REpF8I4OMumi9ONGKsuxGzGZuF7QUUsRMSg&oe=694DADA0"
            ],
            "timestamp": "2025-12-18 21:36:00",
            "reactions": {
                "👍": 212,
                "❤": 83,
                "💜": 24
            }
        }
    ]
}

def add_new_data():
    """Add the new data using the API format"""
    
    # Load current data
    if os.path.exists(MESSENGER_FILE):
        with open(MESSENGER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"authors": []}
    
    # Add timestamp
    new_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Find or create channel
    author_id = new_data['author_id']
    source = new_data['source']
    author_exists = False
    channel_exists = False
    
    for author in data.get('authors', []):
        if author.get('author_id') == author_id:
            author_exists = True
            # Check if channel exists
            channel_exists = False
            for channel in author.get('channels', []):
                if channel.get('source') == source:
                    channel_exists = True
                    print(f"Channel already exists for source: {source}")
                    break
            
            if not channel_exists:
                # Add new channel
                new_channel = {
                    'source': source,
                    'Title': new_data['Title'],
                    'Sub_Title': new_data['Sub_Title'],
                    'icon': new_data['icon'],
                    'messages': new_data['messages'],
                    'last_updated': new_data['last_updated']
                }
                author['channels'].insert(0, new_channel)
                print(f"Added new channel to existing author: {new_data['Title']}")
            break
    
    if not author_exists:
        # Create new author
        new_author = {
            'author_id': author_id,
            'author_url': new_data['author_url'],
            'author_name': new_data['Title'],
            'channels': [
                {
                    'source': source,
                    'Title': new_data['Title'],
                    'Sub_Title': new_data['Sub_Title'],
                    'icon': new_data['icon'],
                    'messages': new_data['messages'],
                    'last_updated': new_data['last_updated']
                }
            ]
        }
        data['authors'].insert(0, new_author)
        print(f"Created new author: {new_data['Title']}")
    
    # Final automated cleanup before saving
    data, _ = cleanup_data_structure(data)
    
    # Save
    with open(MESSENGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ Data added successfully!")
    print(f"   - Total authors: {len(data['authors'])}")
    print(f"   - Total channels: {sum(len(auth['channels']) for auth in data['authors'])}")

if __name__ == '__main__':
    add_new_data()
