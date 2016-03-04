#- navigation bar

public_navbar_html = '''
  <div class="jumbotron">
    <h1>Captcha API</h1>      
  </div>
'''

manage_navbar_html = '''

<nav class="navbar-default">
    <div class="container-fluid">

        <div class="navbar-header">  
          <button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#admin_Navbar">   
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>                        
          </button> <!--.navbar-toggle-->
          <a class="navbar-brand" href="/">Captcha API</a>
        </div> <!-- .navbar-header -->

        <div class="collapse navbar-collapse" id="admin_Navbar">  
          <ul class="nav navbar-nav manage_nav">
            <li><a href="/">Public &nbsp;&nbsp;|</a></li>
            <li class="dropdown">
              <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                Manage Data <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/manage/manage_image">Image Data</a></li>
                <li><a href="/manage/manage_user">User Data</a></li>
              </ul>
          </li> <!--.dropdown-->
        </ul>
      </div> 

    </div> <!--.container-fluid-->
  </nav>
  '''

#- home page
home_page_html = '''
<h2>How to Use:</h2>
<h3>Get API Keys:</h3>
<p>First you need to log in with your google account. A button of "Generate API Keys" will show up. You need to click the button to get your publica and private API keys.</p>
<h3>API call to get the image for the captcha:</h3>
<p>http://captcha-1236.appspot.com/getcaptcha/?key={YOU_PUBLIC_KEY}
<br><p>Parameters:
<br><b>key:</b> Your public API key
<br><br>Examples of API call:
<br>http://captcha-1236.appspot.com/getcaptcha/?key=ABCDE
<br><br>API respond:
<br>A JSON object with image link (img_link) and the image id of the captcha:<br>
{'img_link':'http://captcha-1236.appspot.com/render_image?FGHIJK', 'img_id':'FGHIJK'}
<br><br>JSONP request is also supported.</p>

<h3>API call for captcha validation:</h3>
<p>http://captcha-1236.appspot.com/captchavalidation/?key={YOU_PRIVATE_KEY}&img_id={IMAGE_ID}&user_input={USER_INPUT}
<br><br>Parameters:
<br><b>key:</b> Your private API key, <b>img_id:</b> the img_id for the captcha image, <b>user_input:</b> the input from the user
<br><br>Examples of API call:
<br>http://captcha-1236.appspot.com/captchavalidation/?key=abcde&img_id=FGHIJK&user_input=123
<br><br>API respond:
<br>A JSON object with information of the captcha validation:<br>
{'result':'correct'} or {'result':'incorrect'} or {'result':'Error! Invalid API Key.'} or {'result':'Error! Invalid Image ID.'}</p>
'''

login_home_page_html = home_page_html  + '''
<hr>
<h3>Your public key: [! public_key !]</h3>
<h3>Your private key: [! private_key !]</h3>
<hr>
<p>To generate new keys, please use the following button:</p>
<button ng-click="generate_keys()" class="btn btn-default">Generate API Keys</button>
'''

login_page_html = ''''''

manage_image_page_html = '''
<a href="/manage/add_image"><button class="btn btn-default">Add a Image</button></a>
<hr>
<h3>Total of [!image_data.length!] records</h3>
<div class="table-responsive">
<table class="table data_table">
  <tr>
    <td> Image_ID</td>
    <td> Preview </td>
    <td> Answer </td> 
    <td> Delete </td>
  </tr>

  <tr ng-repeat="item in image_data">
    <td> [! item.img_id !]</td>
    <td><img ng-src="/render_image?[!item.img_id!]"></td> 
    <td> [! item.answer !] </td> 
    <td class="del_mark" ng-click="delete(item.img_id)">X</td>    
  </tr>
</table>
</div> <!--.table-responsive-->
'''

add_image_page_html = '''
<form name="add_photo_form" method="post" action="/manage/add_to_image_db" enctype="multipart/form-data">
  <h3>Add Image</h3> 

  <div class="form-group">
    <label>Answer*</label>
    <input class="form-control" type="text" name="answer" required>
  </div><!-- .form-group -->

  <div class="form-group">
    <a class="btn btn-default" onclick="$('input[name=image_file]').click();">Attachd Image File*</a>
    <input type="file" name="image_file" required>
    <span id="image_file_path"></span>
  </div><!-- .form-group -->

  <input type="reset" class="btn btn-default" value="Reset">
  <input type="submit" class="btn btn-default" name="submit" value="Add">
</form>
'''

manage_user_page_html = '''
<h3>Totol of [!user_data.length!] records</h3>
<div class="table-responsive">
  <table class="table data_table">
    <tr>
      <td> Email </td>
      <td> Public Key </td>
      <td> Private Key </td>
      <td> Delete </td>
    </tr>

    <tr ng-repeat="item in user_data ">
      <td> [! item.email !] </td>
      <td> [! item.public_key !] </td>
      <td> [! item.private_key !] </td>
      <td class="del_mark" ng-click="delete(item.email)">X</td>    
    </tr>
  </table>
</div> <!--.table-responsive-->
'''