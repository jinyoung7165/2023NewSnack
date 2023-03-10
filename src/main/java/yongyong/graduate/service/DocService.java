package yongyong.graduate.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.docDomain.DocRepository;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DocService {

    private final DocRepository docRepository;

    public List<Doc> getAllDocs() {
        return docRepository.findAll();
    }
}
