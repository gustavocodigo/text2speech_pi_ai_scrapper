from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import datetime


import os


import warnings

# Suprimir todos os avisos
warnings.filterwarnings("ignore")

# Seletivamente suprimir os avisos específicos do Selenium (substitua o nome do módulo do Selenium e o aviso específico)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="selenium")




def is_cloudflare_page(driver):
    return "Cloudflare" in driver.page_source



def click_checkbox_cloudflare(driver):
    try:
        checkbox_element = driver.find_element_by_xpath("//*[@id='challenge-stage']/div/label/input")
        if not checkbox_element.is_selected():
            checkbox_element.click()
        return True
    except:
        return False


def click_pass_cloudflare(driver):
    if is_cloudflare_page(driver) == True:
        click_checkbox_cloudflare(driver)




def convert_to_audio(text, path, driverv = None):

    script = """
    (function () {
        const hooks = []
        const oFetch = fetch;

        async function monitorFetch(input, init) {
            let fret = await oFetch(input, init);
            for (let i = 0; i < hooks.length; i++) {
                try {
                    await hooks[i](fret)
                } catch (e) {
                }
            }
            return fret
        }
        fetch = monitorFetch
       let sf = true
       
        hooks.push(async function (response) {
            if (response.ok) {
               if (sf == false){
                    sf = true
                    return
               }
                console.log(response.body)
                const reader = response.body.getReader()
                let done = false;

                const decoder = new TextDecoder('utf-8');
                let text = ""
                var sid = undefined
               let l = 1
                while (done == false) {
		   let ret = await reader.read()
                    if (  l < 1 ) { l = l+1; continue; }
                    done = ret.done
                    text += decoder.decode(ret.value) 
                }
               const regex = /"sid":"([^"]+)"/g;
               const matches = text.match(regex);
               if ( matches) {
                   sid = matches[0].substring(7, matches[0].length - 1)
	       }
               document.body.innerText = "https://pi.ai/api/chat/voice?mode=eager&voice=voice4&messageSid="+sid
               document.body.message = text
            }
        })
    })()
  """

    driver = None
    if ( driverv == None):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--lang=pt-BR")
        options.add_experimental_option("prefs", {
            "download.default_directory": path
        })

        options.add_argument("--lang=pt")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument(
        f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 Edg/88.0.705.74')

        driver = webdriver.Chrome("./driver/chromedriver", options=options)
        driver.delete_all_cookies()

        driver.get("https://pi.ai/talk")
    else:
        driver = driverv
    elemento = False

    # driver.get_screenshot_as_file("screenshot.png")
    count = 0
    while elemento == False:
        try:
            elemento = driver.find_element(By.XPATH, '//*[@enterkeyhint="send"]')
            break
        except Exception as e:
            click_pass_cloudflare(driver)
            # print(e)
            # print("trying again")
            if ( count > 5):
                return ""
            time.sleep(0.1)
            count += 0.1
    driver.execute_script(script)
   
    time.sleep(1)

    count = 0
    while True:
        try:
            elemento.send_keys(text.replace("\n", ","))
            elemento.send_keys(Keys.ENTER)
            body_element = driver.find_element(By.TAG_NAME, 'body')
            while not body_element.text.startswith("https://"):
                time.sleep(0.05)
                count += 0.05
                if count > 10:
                    print("Timeout Exceded.")
                    return ""
            break
        except Exception as e:
            print(e)
            time.sleep(0.2)

    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_text = body_element.text

    javascript_code = """
const link = document.createElement('a');
link.href = arguments[0];
link.setAttribute('download', arguments[1]); // Define o nome do arquivo
document.body.appendChild(link);
link.click();
 """
    current_date = datetime.datetime.now()

    filename = "audio-" + current_date.strftime("%Y-%m-%d-%H-%M-%S") + "-file.mp3"
    filepath = os.path.join(path, filename)
    print(filepath)
    driver.execute_script(javascript_code, body_text, filename)

    while not os.path.exists(filepath):
        time.sleep(0.3)
        # print("Waiting for download: "+filepath)

    if(driverv == None):
        driver.close()
    
    return filepath







from flask import Flask, abort, jsonify, render_template, request

from flask import Flask, send_file
app = Flask(__name__)







options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("--lang=pt-BR")
options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd()+"/audios"
})
options.add_argument("--lang=pt")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome("./driver/chromedriver", options=options)




@app.route('/generate_mp3', methods=['GET'])
def generate_mp3():
    text = request.args.get('text')

    driver.get("https://pi.ai/talk")

    path = convert_to_audio(text, os.getcwd()+"/audios/", driver)
    if ( path == "" ):
        abort(404)
        return
    data = {
        'id': os.path.basename(path)
    }
    return jsonify(data) 




@app.route('/read_file', methods=['GET'])
def read_file():
    path = request.args.get('file')
    if ( path == "" ):
        abort(404)
    print("REQUISITANDO: "+path)
    return send_file("audios/"+os.path.basename(path))





@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')





if __name__ == '__main__':
    app.run(debug)

