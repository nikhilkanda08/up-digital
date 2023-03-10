import os
import time
import random
import logging
from selenium import webdriver
from selenium_stealth import stealth
# import undetected_chromedriver as uc
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger('__name__')

def time_to_visit_final(time_to_visit):
    time_before = time_to_visit-10
    time_after = time_to_visit+10
    final_time = random.randint(time_before, time_after)
    return final_time

def map_search(keyword,website_link,country,state,city,time_to_visit,page_visit_no,search_device_type):
    try:
        knowledge_panel_found = False
        time_total = time_to_visit/page_visit_no
        found_website_in_map = False
        loop_break = False
        found_in_mappack = False
        direction_found = False
        all_pages_link_web_find = []
        visit_pages_on_web = []
        map_page = ""
        ports = [9000, 9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9009, 9010, 9011, 9012, 9013, 9014, 9015, 9016, 9017, 9018, 9019, 9020, 9021, 9022, 9023, 9024, 9025, 9026, 9027, 9028, 9029, 9030, 9031, 9032, 9033, 9034, 9035, 9036, 9037, 9038, 9039, 9040, 9041, 9042, 9043, 9044, 9045, 9046, 9047, 9048, 9049, 9050, 9051, 9052, 9053, 9054, 9055, 9056, 9057, 9058, 9059, 9060, 9061, 9062, 9063, 9064, 9065, 9066, 9067, 9068, 9069, 9070, 9071, 9072, 9073, 9074, 9075, 9076, 9077, 9078, 9079, 9080, 9081, 9082, 9083, 9084, 9085, 9086, 9087, 9088, 9089, 9090, 9091, 9092, 9093, 9094, 9095, 9096, 9097, 9098, 9099, 9100, 9101, 9102, 9103, 9104, 9105, 9106, 9107, 9108, 9109, 9110, 9111, 9112, 9113, 9114, 9115, 9116, 9117, 9118, 9119, 9120, 9121, 9122, 9123, 9124, 9125, 9126, 9127, 9128, 9129, 9130, 9131, 9132, 9133, 9134, 9135, 9136, 9137, 9138, 9139, 9140, 9141, 9142, 9143, 9144, 9145, 9146, 9147, 9148, 9149, 9150, 9151, 9152, 9153, 9154, 9155, 9156, 9157, 9158, 9159, 9160, 9161, 9162, 9163, 9164, 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175, 9176, 9177, 9178, 9179, 9180, 9181, 9182, 9183, 9184, 9185, 9186, 9187, 9188, 9189, 9190, 9191, 9192, 9193, 9194, 9195, 9196, 9197, 9198, 9199, 9200, 9201, 9202, 9203, 9204, 9205, 9206, 9207, 9208, 9209, 9210, 9211, 9212, 9213, 9214, 9215, 9216, 9217, 9218, 9219, 9220, 9221, 9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230, 9231, 9232, 9233, 9234, 9235, 9236, 9237, 9238, 9239, 9240, 9241, 9242, 9243, 9244, 9245, 9246, 9247, 9248, 9249, 9250, 9251, 9252, 9253, 9254, 9255, 9256, 9257, 9258, 9259, 9260, 9261, 9262, 9263, 9264, 9265, 9266, 9267, 9268, 9269, 9270, 9271, 9272, 9273, 9274, 9275, 9276, 9277, 9278, 9279, 9280, 9281, 9282, 9283, 9284, 9285, 9286, 9287, 9288, 9289, 9290, 9291, 9292, 9293, 9294, 9295, 9296, 9297, 9298, 9299, 9300, 9301, 9302, 9303, 9304, 9305, 9306, 9307, 9308, 9309, 9310, 9311, 9312, 9313, 9314, 9315, 9316, 9317, 9318, 9319, 9320, 9321, 9322, 9323, 9324, 9325, 9326, 9327, 9328, 9329, 9330, 9331, 9332, 9333, 9334, 9335, 9336, 9337, 9338, 9339, 9340, 9341, 9342, 9343, 9344, 9345, 9346, 9347, 9348, 9349, 9350, 9351, 9352, 9353, 9354, 9355, 9356, 9357, 9358, 9359, 9360, 9361, 9362, 9363, 9364, 9365, 9366, 9367, 9368, 9369, 9370, 9371, 9372, 9373, 9374, 9375, 9376, 9377, 9378, 9379, 9380, 9381, 9382, 9383, 9384, 9385, 9386, 9387, 9388, 9389, 9390, 9391, 9392, 9393, 9394, 9395, 9396, 9397, 9398, 9399, 9400, 9401, 9402, 9403, 9404, 9405, 9406, 9407, 9408, 9409, 9410, 9411, 9412, 9413, 9414, 9415, 9416, 9417, 9418, 9419, 9420, 9421, 9422, 9423, 9424, 9425, 9426, 9427, 9428, 9429, 9430, 9431, 9432, 9433, 9434, 9435, 9436, 9437, 9438, 9439, 9440, 9441, 9442, 9443, 9444, 9445, 9446, 9447, 9448, 9449, 9450, 9451, 9452, 9453, 9454, 9455, 9456, 9457, 9458, 9459, 9460, 9461, 9462, 9463, 9464, 9465, 9466, 9467, 9468, 9469, 9470, 9471, 9472, 9473, 9474, 9475, 9476, 9477, 9478, 9479, 9480, 9481, 9482, 9483, 9484, 9485, 9486, 9487, 9488, 9489, 9490, 9491, 9492, 9493, 9494, 9495, 9496, 9497, 9498,
            9499, 9500, 9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509, 9510, 9511, 9512, 9513, 9514, 9515, 9516, 9517, 9518, 9519, 9520, 9521, 9522, 9523, 9524, 9525, 9526, 9527, 9528, 9529, 9530, 9531, 9532, 9533, 9534, 9535, 9536, 9537, 9538, 9539, 9540, 9541, 9542, 9543, 9544, 9545, 9546, 9547, 9548, 9549, 9550, 9551, 9552, 9553, 9554, 9555, 9556, 9557, 9558, 9559, 9560, 9561, 9562, 9563, 9564, 9565, 9566, 9567, 9568, 9569, 9570, 9571, 9572, 9573, 9574, 9575, 9576, 9577, 9578, 9579, 9580, 9581, 9582, 9583, 9584, 9585, 9586, 9587, 9588, 9589, 9590, 9591, 9592, 9593, 9594, 9595, 9596, 9597, 9598, 9599, 9600, 9601, 9602, 9603, 9604, 9605, 9606, 9607, 9608, 9609, 9610, 9611, 9612, 9613, 9614, 9615, 9616, 9617, 9618, 9619, 9620, 9621, 9622, 9623, 9624, 9625, 9626, 9627, 9628, 9629, 9630, 9631, 9632, 9633, 9634, 9635, 9636, 9637, 9638, 9639, 9640, 9641, 9642, 9643, 9644, 9645, 9646, 9647, 9648, 9649, 9650, 9651, 9652, 9653, 9654, 9655, 9656, 9657, 9658, 9659, 9660, 9661, 9662, 9663, 9664, 9665, 9666, 9667, 9668, 9669, 9670, 9671, 9672, 9673, 9674, 9675, 9676, 9677, 9678, 9679, 9680, 9681, 9682, 9683, 9684, 9685, 9686, 9687, 9688, 9689, 9690, 9691, 9692, 9693, 9694, 9695, 9696, 9697, 9698, 9699, 9700, 9701, 9702, 9703, 9704, 9705, 9706, 9707, 9708, 9709, 9710, 9711, 9712, 9713, 9714, 9715, 9716, 9717, 9718, 9719, 9720, 9721, 9722, 9723, 9724, 9725, 9726, 9727, 9728, 9729, 9730, 9731, 9732, 9733, 9734, 9735, 9736, 9737, 9738, 9739, 9740, 9741, 9742, 9743, 9744, 9745, 9746, 9747, 9748, 9749, 9750, 9751, 9752, 9753, 9754, 9755, 9756, 9757, 9758, 9759, 9760, 9761, 9762, 9763, 9764, 9765, 9766, 9767, 9768, 9769, 9770, 9771, 9772, 9773, 9774, 9775, 9776, 9777, 9778, 9779, 9780, 9781, 9782, 9783, 9784, 9785, 9786, 9787, 9788, 9789, 9790, 9791, 9792, 9793, 9794, 9795, 9796, 9797, 9798, 9799, 9800, 9801, 9802, 9803, 9804, 9805, 9806, 9807, 9808, 9809, 9810, 9811, 9812, 9813, 9814, 9815, 9816, 9817, 9818, 9819, 9820, 9821, 9822, 9823, 9824, 9825, 9826, 9827, 9828, 9829, 9830, 9831, 9832, 9833, 9834, 9835, 9836, 9837, 9838, 9839, 9840, 9841, 9842, 9843, 9844, 9845, 9846, 9847, 9848, 9849, 9850, 9851, 9852, 9853, 9854, 9855, 9856, 9857, 9858, 9859, 9860, 9861, 9862, 9863, 9864, 9865, 9866, 9867, 9868, 9869, 9870, 9871, 9872, 9873, 9874, 9875, 9876, 9877, 9878, 9879, 9880, 9881, 9882, 9883, 9884, 9885, 9886, 9887, 9888, 9889, 9890, 9891, 9892, 9893, 9894, 9895, 9896, 9897, 9898, 9899, 9900, 9901, 9902, 9903, 9904, 9905, 9906, 9907, 9908, 9909, 9910, 9911, 9912, 9913, 9914, 9915, 9916, 9917, 9918, 9919, 9920, 9921, 9922, 9923, 9924, 9925, 9926, 9927, 9928, 9929, 9930, 9931, 9932, 9933, 9934, 9935, 9936, 9937, 9938, 9939, 9940, 9941, 9942, 9943, 9944, 9945, 9946, 9947, 9948, 9949, 9950, 9951, 9952, 9953, 9954, 9955, 9956, 9957, 9958, 9959, 9960, 9961, 9962, 9963, 9964, 9965, 9966, 9967, 9968, 9969, 9970, 9971, 9972, 9973, 9974, 9975, 9976, 9977, 9978, 9979, 9980, 9981, 9982, 9983, 9984, 9985, 9986, 9987, 9988, 9989, 9990, 9991, 9992, 9993, 9994, 9995, 9996, 9997, 9998, 9999]
        random_port = random.choice(ports)


        screen_resolutions = [["T",340, 695],["L",1366,768],["P",412,914]]
        random_resolution = screen_resolutions[search_device_type]
        device = random_resolution[0]
        width = random_resolution[1]
        height = random_resolution[2]

        proxy_options = {
            'proxy': {
                'http': f'http://Oi4iUEKjgm7Q5r1f:wifi;{country};;{state};{city}@rotating.proxyempire.io:'+f'{random_port}',
                'https': f'https://Oi4iUEKjgm7Q5r1f:wifi;{country};;{state};{city}@rotating.proxyempire.io:'+f'{random_port}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

        enter_keyword = keyword
        website_link = website_link
        prefs = {"profile.managed_default_content_settings.images": 2}
        options = uc.ChromeOptions()
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        chrome_driver = uc.Chrome(
            options=options, 
            seleniumwire_options=proxy_options,
            use_subprocess=True
            )
        chrome_driver.set_window_size(width, height)

        stealth(chrome_driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        chrome_driver.delete_all_cookies()
        chrome_driver.execute_script(
            'videos = document.querySelectorAll("video"); for(video of videos) {video.pause()}')
        chrome_driver.get("https://www.google.com/")
        chrome_driver.find_element(
            'xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(enter_keyword)
        chrome_driver.find_element(
            'xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

        # knowledge panel
        try:
            
            web_btn = chrome_driver.find_elements(By.CSS_SELECTOR,"a.ab_button")
            for c,btn in enumerate(web_btn):
                web_btn = chrome_driver.find_elements(By.CSS_SELECTOR,"a.ab_button")[c].get_attribute("href")
                if website_link in web_btn:
                    knowledge_panel_found = True
                    web_btn = chrome_driver.find_elements(By.CSS_SELECTOR,"a.ab_button")[c].click()
                    time.sleep(10)
                    link_match_web = []
                    all_link_on_web = chrome_driver.find_elements(By.TAG_NAME, "a")
                    for link in all_link_on_web:
                        try:
                            if website_link in link.get_attribute("href"):
                                site_found_status = True
                                if link.get_attribute("href") not in link_match_web:
                                    link_match_web.append(link.get_attribute("href"))
                        except:
                            continue
                    if len(link_match_web) >= page_visit_no:
                        for i in range(page_visit_no):
                            random_link = random.choice(link_match_web)
                            if random_link  != None and random_link != "":
                                if website_link in random_link and "mailto:" not in random_link and "tel:" not in random_link :
                                    print(f"random visit of your site {random_link}")
                                    chrome_driver.get(random_link)
                                    ran_time = time_to_visit_final(time_total)
                                    time.sleep(ran_time)
                                    visit_pages_on_web.append([chrome_driver.title,chrome_driver.current_url,ran_time])
                                    chrome_driver.execute_script(
                                        "window.scrollTo(0,document.body.scrollHeight)")


        except Exception as ex:
            print(ex)
            pass
        # knowledge_panel_end
        
        
        
        
        if knowledge_panel_found == False:
            ### check in mappack 
            try:
                all_map_pack_list = chrome_driver.find_elements(By.CSS_SELECTOR,'a.tiS4rf.Q2MMlc')
                for index,map_pack_list in enumerate(all_map_pack_list):
                    web_in_map_pack_name = chrome_driver.find_elements(By.CSS_SELECTOR,'div.dbg0pd')[index].text.strip()
                    web_in_map_pack_link = chrome_driver.find_elements(By.CSS_SELECTOR,'a.yYlJEf.Q7PwXb.L48Cpd')[index].get_attribute("href")
                    if website_link in  web_in_map_pack_link:
                        
                        web_in_map_pack_link = chrome_driver.find_elements(By.CSS_SELECTOR,'a.yYlJEf.Q7PwXb.L48Cpd')[index].click()
                        found_in_mappack = True
                        time.sleep(5)
                        all_pages_link = chrome_driver.find_elements(By.TAG_NAME,"a")
                        for page_index,page in enumerate(all_pages_link,1):
                            all_pages_link_web_find.append(page.get_attribute("href"))
                        if len(all_pages_link_web_find) >= page_visit_no:
                            for i in range(page_visit_no):
                                random_link = random.choice(all_pages_link_web_find)
                                if random_link  != None and random_link != "":
                                    if website_link in random_link and "mailto:" not in random_link and "tel:" not in random_link :
                                        chrome_driver.get(random_link)
                                        ran_time = time_to_visit_final(time_total)
                                        time.sleep(ran_time)
                                        visit_pages_on_web.append([chrome_driver.title,random_link,ran_time])
                                        chrome_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            except Exception as ex:
                pass


        if found_in_mappack == False and knowledge_panel_found == False:
            click_more_place = chrome_driver.find_elements(By.CSS_SELECTOR,'a.tiS4rf')
            for index_b,more_places in enumerate(click_more_place):
                more_places_text = chrome_driver.find_elements(By.CSS_SELECTOR,'a.tiS4rf')[index_b].text.strip()
                if "More places" in more_places_text or  "More businesses" in more_places_text:
                    more_places_text = chrome_driver.find_elements(By.CSS_SELECTOR,'a.tiS4rf')[index_b].click()
                    all_pages = 10
                    i = 1
                    while i <= all_pages:
                        try:
                            if i != 1:
                                click_on_page = chrome_driver.find_elements(By.CSS_SELECTOR,"a.fl")[i].click()
                            time.sleep(3)
                            for index_map in range(0,20):
                                try:
                                    element = chrome_driver.find_elements(By.CSS_SELECTOR,"div.dbg0pd")[index_map]
                                    actions = ActionChains(chrome_driver)
                                    actions.move_to_element(element).perform()
                                    map_website = chrome_driver.find_elements(By.CSS_SELECTOR,"a.yYlJEf.Q7PwXb.L48Cpd")[index_map].get_attribute("href")
                                    if website_link in map_website:
                                        
                                        found_website_in_map = True
                                        loop_break = True
                                        if found_website_in_map:
                                            map_page = i
                                            map_website = chrome_driver.find_elements(By.CSS_SELECTOR,"a.yYlJEf.Q7PwXb.L48Cpd")[index_map].click()
                                            time.sleep(5)
                                            all_pages_link = chrome_driver.find_elements(By.TAG_NAME,"a")
                                            for page_index,page in enumerate(all_pages_link,1):
                                                all_pages_link_web_find.append(page.get_attribute("href"))
                                            if len(all_pages_link_web_find) >= page_visit_no:
                                                for i in range(page_visit_no):
                                                    random_link = random.choice(all_pages_link_web_find)
                                                    if random_link  != None and random_link != "":
                                                        if website_link in random_link and "mailto:" not in random_link and "tel:" not in random_link :
                                                            chrome_driver.get(random_link)
                                                            ran_time = time_to_visit_final(time_total)
                                                            time.sleep(ran_time)
                                                            visit_pages_on_web.append([chrome_driver.title,random_link,ran_time])
                                                            chrome_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")                    
                                except:
                                    pass
                        except:
                            pass
                        if loop_break:
                            break
                        i+=1 
        
        logger.debug(f'keyword =>{keyword}, website_link =>{website_link}, time_to_visit =>{time_to_visit}, country =>{country}, city =>{city}, state =>{state}')
        logger.debug(f'found_website_in_map =>{found_website_in_map},found_in_mappack =>{found_in_mappack},map_page =>{map_page},visit_pages_on_web length =>{len(visit_pages_on_web)},search_device_type =>{search_device_type},direction_found =>{direction_found},knowledge_panel_found =>{knowledge_panel_found}')
        return found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,direction_found,search_device_type,knowledge_panel_found
    except Exception as e:
        print(e)
        logger.debug(f'keyword =>{keyword}, website_link =>{website_link}, country =>{country}, city =>{city}, state =>{state}, search_device_type=>{search_device_type}')
        logger.debug(f'Bot Error =>{e}')
        
        return False,False,[],0,False,search_device_type,False
