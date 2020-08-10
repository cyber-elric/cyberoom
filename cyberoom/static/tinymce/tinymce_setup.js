tinymce.init({
    // 选择id为content的标签作为编辑器
    selector: '#rich_content',
    // 语言选择中文
    language:'zh_CN',

    height: 444,
    width: '100%',

    // 工具栏上面的补丁按钮
    plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'save table contextmenu directionality template paste textcolor',
            'codesample',
    ],
    // 工具栏的补丁按钮
    toolbar: 'fullscreen preview | undo redo | codesample link image media | bold italic forecolor backcolor  fontsizeselect | alignleft aligncenter alignright alignjustify bullist numlist outdent indent',

    automatic_uploads: true,
    images_upload_url: "/pensieve/up/",

    // 字体大小
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
});
