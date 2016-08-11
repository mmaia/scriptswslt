    <head>
        <script type="text/javascript">
            dojo.event.topic.subscribe("/edit", function(data, type,
request) {
            alert("type: "+type);
            alert("data: "+data);
            if(type="load"){
                document.getElementById("result").innerHTML=data;
            }
           
            });
        </script>
    </head>

<!-- URL link to struts action-->
<s:url id="ajaxText" action="ajax" method="ajax" >
<s:param name="decorate" value="false" />
</s:url> 

<!-- Div where content will be displayed -->
<s:div theme="ajax" id="weather" href="${ajaxText}">
    loading content... from the ajax action the ajax method is called.
than the ajaxReturn.jsp is rendered here.
</s:div>


<p>Persons</p>
<s:if test="persons.size > 0">
    <table>
        <s:iterator value="persons">
            <tr id="row_<s:property value="id"/>">
                <td>
                    <s:property value="firstName" />
                </td>
                <td>
                    <s:property value="lastName" />
                </td>
                <td>
                <!-- call the remove method on the ajax action no return-->
                    <s:url id="removeUrl" action="ajax" method="remove">
                        <s:param name="id" value="id" />
                        <s:param name="decorate" value="false" />
                    </s:url>
                    <s:a href="%{removeUrl}" theme="ajax" >Remove</s:a>
                   
                    <!-- call the edit method an the ajax action. the
result (ajaxResult.jps)
                    will be handed to the edit javascript mothed
attached to dojo (above) -->
                    <s:url id="editUrl" action="ajax" method="ajax">
                        <s:param name="id" value="id" />
                        <s:param name="decorate" value="false" />
                    </s:url>
                    <s:a href="%{editUrl}" id="a_%{id}" theme="ajax"
notifyTopics="/edit">Edit</s:a>
                </td>
                <td>
                <a href=ajax!remove.html?id=2>remove me no ajax</a>
                </td>
            </tr>
        </s:iterator>
    </table>
</s:if>

<hr>
<div id=result></div>