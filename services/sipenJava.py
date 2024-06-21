def menuIrpara(url, driver):
    driver.execute_script(f"function menuIrPara({url})" +
                          """{
                                        var
                                    iframe;
                                    if (url.indexOf("Login.do") != -1) {
                                    iframe = window.parent.parent.frames["principal"];
                                    } else {
                                    iframe = window.frames["iframe01"];
                                    }
                                    iframe.location.href = CONTEXT + url;
                                    }""" +
                          f"menuIrPara({url})"

                          )
