1. Purpose: login the Unified identity authentication system of South China University of Technology

        Warning: Do not use for illegal purposes!

2. Requirements: execjs 
 
        pip install pyexecjs

3. Call function:

    (1) Method:

        from scutlogin.login import *
        GetLoginState().login(un, pd, server_url)

    (2) Parameter description:

        un --> student number
        pd --> student password
        server_url --> service url

    (3) Rules of service url:

        https://sso.scut.edu.cn/cas/login? --> location of unified identity authentication system
        service=server_url --> the server url you need

    (4) Examples:

        IAmOK --> https://sso.scut.edu.cn/cas/login?service=https://iamok.scut.edu.cn/cas/login
        Integrated information service --> https://sso.scut.edu.cn/cas/login?service=https://my.scut.edu.cn/up/
        Student educational administration system (2018) --> https://sso.scut.edu.cn/cas/login?service=http://jw2018.jw.scut.edu.cn/sso/driotlogin
 
    (5) If login is successful:

        Directly use <r.post> or <r.get> to send request