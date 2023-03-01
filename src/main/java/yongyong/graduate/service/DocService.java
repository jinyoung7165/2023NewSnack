package yongyong.graduate.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.docDomain.DocRepository;

import java.util.List;

@Service
public class DocService {

    private final DocRepository docRepository;

    @Autowired
    public DocService(DocRepository docRepository) {
        this.docRepository = docRepository;
    }

    public List<Doc> getAllDocs() {
        return docRepository.findAll();
    }
}
